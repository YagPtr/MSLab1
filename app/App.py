import random
import os
import flet as ft
import matrix
class Page(ft.Column):
    def __init__(self,page:ft.Page):
        def pick_files_result(e: ft.FilePickerResultEvent):
            print(e)

            with open(e.files[0].path, 'r', encoding='utf-8') as file:
                rows = int(file.readline().strip())
                cols = int(file.readline().strip())

                matrix = []
                for _ in range(rows):
                    line = file.readline().strip()
                    matrix.append([float(num) for num in line.split(',')])

                self.table=matrix
                self.change_matrix('')


        def pick_dir(e: ft.FilePickerResultEvent):
            print(e)
            self.dir=e.path




        super().__init__()
        self.page=page
        self.pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
        self.page.overlay.append(self.pick_files_dialog)
        self.button_load_file=ft.ElevatedButton(
                        "Загрузка файла",
                        on_click=lambda _: self.pick_files_dialog.pick_files(
                            allow_multiple=False
                        ),
                    )
        self.pick_files_dialog2 = ft.FilePicker(on_result=pick_dir)
        self.page.overlay.append(self.pick_files_dialog2)

        self.button_chose_dir = ft.ElevatedButton(
            "Выбор директории",
            on_click=lambda _: self.pick_files_dialog2.get_directory_path(),
        )


        self.first_player_amount=ft.TextField(label='Первый',value=5,width=70)
        self.second_player_amount=ft.TextField(label='Второй',value=100,width=70)
        self.max_for_rand=ft.TextField(label='Макс',value=5,width=70)
        self.min_for_rand = ft.TextField(label='Мин', value=0, width=70)
        self.table=[[random.uniform(int(self.min_for_rand.value),int(self.max_for_rand.value) ) for i in range(int(self.second_player_amount.value))] for j in range(int(self.first_player_amount.value))]
        # print(self.table)
        self.button_create_matrix=ft.ElevatedButton("Сгенерировать",on_click=self.update_matrix)
        self.button_load_into_file=ft.ElevatedButton("Записать в файл",on_click=self.write_file)
        self.button_refresh=ft.ElevatedButton("Обновить таблицу",on_click=self.refresh_table)
        self.button_minmax = ft.ElevatedButton("М/М", on_click=self.out_minimax)
        self.ManageButtons=ft.Row([self.button_load_file,self.button_create_matrix,self.button_load_into_file])
        self.ManageButtons2=ft.Row([self.button_minmax,self.button_refresh,self.button_chose_dir])
        self.PlayerRows=ft.Row([self.first_player_amount,self.second_player_amount,self.min_for_rand,self.max_for_rand])
        self.create_matrix('')

        # self.Matrix=matrix.Matrix(22,4)
        # self.controls=[self.PlayerRows,ft.InteractiveViewer(self.Matrix,clip_behavior=ft.ClipBehavior.ANTI_ALIAS,boundary_margin=ft.margin.only(0,0,1000,1000))]



    def create_matrix(self,e):
        print("this one")
        self.table=[[random.uniform(int(self.min_for_rand.value),int(self.max_for_rand.value) ) for i in range(int(self.second_player_amount.value))] for j in range(int(self.first_player_amount.value))]
        self.Matrix=matrix.Matrix(int(self.first_player_amount.value),int(self.second_player_amount.value),self.table)
        self.controls = [ft.Container(ft.Column([self.ManageButtons, self.ManageButtons2, self.PlayerRows]),
                                      offset=ft.Offset(0.03, 0.05)),
                         ft.Row([ft.InteractiveViewer(self.Matrix,
                                                      boundary_margin=ft.margin.only(0, 0, 100000, 100000),width=10000,height=10000)])]

    def update_matrix(self,e):
        print("update")
        self.create_matrix(e)
        self.update()

    def change_matrix(self,e):
        print("another one")
        self.Matrix = matrix.Matrix(int(self.first_player_amount.value), int(self.second_player_amount.value),
                                    self.table)
        self.controls = [ft.Container(ft.Column([self.ManageButtons, self.ManageButtons2, self.PlayerRows]),
                                      offset=ft.Offset(0.03, 0.05)),
                         ft.Row([ft.InteractiveViewer(self.Matrix,
                                                      boundary_margin=ft.margin.only(0, 0, 100000, 100000), width=10000,
                                                      height=10000)])]
        self.update()



    def out_minimax(self,e):
        maximin, maximin_pos, minimax, minimax_pos = self.count_minimax()
        self.page.open(ft.AlertDialog(content=ft.Text(f"Максимин - {maximin}, позиция в таблице - {maximin_pos}\n"
                   f"Минимакс - {minimax}, позиция в таблице - {minimax_pos}\n")))



    def write_file(self,e):
        # whatever = lambda _: self.pick_files_dialog2.get_directory_path()
        # whatever('')
        self.refresh_table('')
        try:
            with open(self.dir+"/file.csv", 'w', encoding='utf-8') as file:

                for i in self.table:
                    for j in i:
                        file.write(str(j)+",")
                    file.write("\n")
                file.write(f"Матрица размерности {self.first_player_amount.value} x {self.second_player_amount.value} \n")
                maximin, maximin_pos, minimax, minimax_pos = self.count_minimax()
                file.write(f"Максимин - {maximin}, позиция в таблице - {maximin_pos}\n"
                           f"Минимакс - {minimax}, позиция в таблице - {minimax_pos}\n")
                self.page.open(ft.AlertDialog(content=ft.Text(f"Данные записаны в файл: {self.dir+"/file.csv"}")))
        except Exception as e:
            self.page.open(ft.AlertDialog(content=ft.Text(e)))




    def count_minimax(self):
        min_in_rows = [min(row) for row in self.table]  # Минимумы по строкам
        maximin_value = max(min_in_rows)  # Максимальный из минимумов
        maximin_position = [(i, row.index(maximin_value)) for i, row in enumerate(self.table) if maximin_value in row]

        max_in_columns = [max(col) for col in zip(*self.table)]  # Максимумы по столбцам
        minimax_value = min(max_in_columns)  # Минимальный из максимумов
        minimax_position = [(col.index(minimax_value), j) for j, col in enumerate(zip(*self.table)) if minimax_value in col]

        return maximin_value, maximin_position, minimax_value, minimax_position

    def refresh_table(self,e):
        matrix=self.Matrix.controls
        for i in range(1,int(self.first_player_amount.value)+1):
            row=matrix[i]
            for j in range(1,int(self.second_player_amount.value)+1):
                # print(row.controls[j].value)
                self.table[i-1][j-1]=row.controls[j].value
            # print("\n")

