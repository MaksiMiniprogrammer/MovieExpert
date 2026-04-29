class MovieExpertModel:
    
    def __init__(self):
        self.data = None

    def set_data(self, data: dict):
        self.data = data

    #ЗДЕСЬ НУЖНО ДОБАВИТЬ ЛОГИКУ ЭКСПЕРТОВ
    def selection_process(self):
        if not self.data:
            return None

        complex_plots = self.data.get("complex_plots", True)
        rewatchable = self.data.get("rewatchable", True)
        arthouse = self.data.get("arthouse", True)
        genre = self.data.get("genre", "")

        if not genre:
            return None

        profile = ""
        depth = ""
        tempo = ""

        movie = None
        if not movie:
            return None

        return {
            "profile": profile,
            "depth": depth,
            "tempo": tempo,
            "movie_title": movie["title"],
            "movie_subtitle": movie["subtitle"],
            "movie_desc": movie["desc"],
            "status": "Рекомендация найдена"
        }