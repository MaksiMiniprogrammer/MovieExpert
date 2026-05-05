import collections
import collections.abc

if not hasattr(collections, 'Mapping'):
    collections.Mapping = collections.abc.Mapping

from experta import KnowledgeEngine, Fact, Rule, NOT


class MovieExpertSystem(KnowledgeEngine):

    def __init__(self):
        super().__init__()
        self.result = None

    def infer(self, data: dict) -> dict:
        self.reset()
        self.result = None

        normalized = self._normalize_input(data)

        self.declare(Fact(complex_plots=normalized["complex_plots"]))
        self.declare(Fact(rewatchable=normalized["rewatchable"]))
        self.declare(Fact(arthouse=normalized["arthouse"]))
        self.declare(Fact(genre=normalized["genre"]))

        self.run()

        if self.result is not None:
            return self.result

        return {
            "profile": "—",
            "depth": "—",
            "tempo": "—",
            "movie_title": "Фильм не найден",
            "movie_subtitle": "",
            "movie_desc": "Нет подходящего сочетания правил для выбранных параметров.",
            "status": "Рекомендация не найдена",
        }


    def _normalize_input(self, data: dict) -> dict:
        return {
            "complex_plots": bool(data.get("complex_plots", False)),
            "rewatchable": bool(data.get("rewatchable", False)),
            "arthouse": bool(data.get("arthouse", False)),
            "genre": (data.get("genre") or "").strip().lower(),
        }

    # -------------------------
    # Helpers
    # -------------------------
    def _set_profile(self, profile: str):
        """
        Ставит промежуточный профиль и блокирует повторный выбор.
        """
        if self.get_result_marker("profile_set"):
            return
        self.declare(Fact(profile=profile))
        self.declare(Fact(profile_set=True))

    def _set_loading(self, depth: str, tempo: str):
        if self.get_result_marker("loading_set"):
            return
        self.declare(Fact(depth=depth))
        self.declare(Fact(tempo=tempo))
        self.declare(Fact(loading_set=True))

    def _set_final_result(
        self,
        profile: str,
        depth: str,
        tempo: str,
        movie_title: str,
        movie_subtitle: str,
        movie_desc: str,
    ):
        if self.get_result_marker("result_set"):
            return

        self.result = {
            "profile": profile,
            "depth": depth,
            "tempo": tempo,
            "movie_title": movie_title,
            "movie_subtitle": movie_subtitle,
            "movie_desc": movie_desc,
            "status": "Рекомендация найдена",
        }
        self.declare(Fact(result_set=True))

    def get_result_marker(self, marker_name: str) -> bool:
        return any(
            isinstance(fact, Fact) and fact.get(marker_name) is True
            for fact in self.facts.values()
        )

    # -------------------------
    # Level 1: profile
    # -------------------------
    @Rule(
        Fact(complex_plots=True),
        Fact(rewatchable=True),
        Fact(arthouse=True),
        NOT(Fact(profile_set=True)),
        salience=30,
    )
    def rule_1_kinoestet(self):
        self._set_profile("Киноэстет")

    @Rule(
        Fact(complex_plots=True),
        Fact(rewatchable=False),
        NOT(Fact(profile_set=True)),
        salience=20,
    )
    def rule_2_novice_rewatch_no(self):
        self._set_profile("Любознательный новичок")

    @Rule(
        Fact(complex_plots=True),
        Fact(arthouse=False),
        NOT(Fact(profile_set=True)),
        salience=20,
    )
    def rule_2_novice_arthouse_no(self):
        self._set_profile("Любознательный новичок")

    @Rule(
        Fact(complex_plots=False),
        NOT(Fact(profile_set=True)),
        salience=10,
    )
    def rule_3_mass_no_complex(self):
        self._set_profile("Массовый зритель")

    @Rule(
        Fact(complex_plots=True),
        Fact(rewatchable=False),
        Fact(arthouse=False),
        NOT(Fact(profile_set=True)),
        salience=9,
    )
    def rule_3_mass_complex_no_no(self):
        self._set_profile("Массовый зритель")

    # -------------------------
    # Level 2: depth / tempo
    # -------------------------
    @Rule(Fact(profile="Киноэстет"), NOT(Fact(loading_set=True)), salience=20)
    def rule_4_kinoestet_loading(self):
        self._set_loading("высокая", "медленный")

    @Rule(Fact(profile="Любознательный новичок"), NOT(Fact(loading_set=True)), salience=20)
    def rule_5_newbie_loading(self):
        self._set_loading("средняя", "средний")

    @Rule(Fact(profile="Массовый зритель"), NOT(Fact(loading_set=True)), salience=20)
    def rule_6_mass_loading(self):
        self._set_loading("низкая", "быстрый")

    # -------------------------
    # Level 3: final movie
    # -------------------------
    @Rule(
        Fact(depth="высокая"),
        Fact(tempo="медленный"),
        Fact(genre="драма"),
        NOT(Fact(result_set=True)),
        salience=5,
    )
    def rule_7_seventh_seal(self):
        self._set_final_result(
            profile="Киноэстет",
            depth="высокая",
            tempo="медленный",
            movie_title="Седьмая печать",
            movie_subtitle="The Seventh Seal (1957)",
            movie_desc=(
                "Рыцарь Антониус Блок возвращается из крестового похода "
                "и встречает Смерть. Их партия в шахматы определит его судьбу."
            ),
        )

    @Rule(
        Fact(depth="средняя"),
        Fact(tempo="средний"),
        Fact(genre="фантастика"),
        NOT(Fact(result_set=True)),
        salience=5,
    )
    def rule_8_interstellar(self):
        self._set_final_result(
            profile="Любознательный новичок",
            depth="средняя",
            tempo="средний",
            movie_title="Интерстеллар",
            movie_subtitle="Interstellar (2014)",
            movie_desc=(
                "История о миссии через космос, где на первом месте "
                "остаются выбор, время и связь между людьми."
            ),
        )

    @Rule(
        Fact(depth="низкая"),
        Fact(tempo="быстрый"),
        Fact(genre="боевик"),
        NOT(Fact(result_set=True)),
        salience=5,
    )
    def rule_9_terminator_2(self):
        self._set_final_result(
            profile="Массовый зритель",
            depth="низкая",
            tempo="быстрый",
            movie_title="Терминатор 2",
            movie_subtitle="Terminator 2: Judgment Day (1991)",
            movie_desc=(
                "Динамичный фантастический боевик о противостоянии "
                "людей и машины будущего."
            ),
        )

    @Rule(
        Fact(depth="низкая"),
        Fact(tempo="быстрый"),
        Fact(genre="романтическая комедия"),
        NOT(Fact(result_set=True)),
        salience=5,
    )
    def rule_10_pretty_woman(self):
        self._set_final_result(
            profile="Массовый зритель",
            depth="низкая",
            tempo="быстрый",
            movie_title="Красотка",
            movie_subtitle="Pretty Woman (1990)",
            movie_desc=(
                "Романтическая история с лёгким темпом и понятным сюжетом."
            ),
        )

class MovieExpertModel:
    def __init__(self):
        self._data = None
        self._engine = MovieExpertSystem()

    def set_data(self, data: dict):
        self._data = data

    def selection_process(self):
        res = self._engine.infer(self._data)
        if res.get("status") == "Рекомендация найдена":
            return res
        return None