class MovieExpertController:
    
    def __init__(self, model, view):
        self.view = view
        self.model = model
        self.view.set_controller(self)

    def handle_submit(self, data: dict):
        print("Получены данные из View:")
        print(data)
        self.model.set_data(data)
        result = self.model.selection_process()
        if result:
            self.view.show_result(result)
        else:
            self.view.clear_result()

    def handle_reset(self):
        print("Форма сброшена")
        self.view.clear_result()
