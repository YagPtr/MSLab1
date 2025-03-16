import flet as ft

class Matrix(ft.Column):
    def __init__(self,first,second,matrix):
        super().__init__()
        self.controls.append(ft.Row(
            [ft.TextField(read_only=True, width=70)] + [ft.TextField(str(k) + " В", read_only=True, width=70) for k in
                                                        range(second)]))

        for i in range(first):
            temp=ft.Row([ft.TextField(str(i)+" В",read_only=True,width=70)])
            for j in range(second):
                temp.controls.append(ft.TextField("{:.2f}".format(matrix[i][j]),width=70))
            self.controls.append(temp)