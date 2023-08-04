import tkinter as tk
from tkinter import ttk
import sqlite3
import functions_sql as fsql
import functions_ui as fui
import functions_file as ff
        
fields_2d_file = 'fields_2d.txt'
texts_2d_file = 'texts_2d.txt'
table_names_file = 'table_names.txt'
temp_value = 'temp_value.txt'

ff.create_file_if_not_exists(fields_2d_file)
ff.create_file_if_not_exists(texts_2d_file)
ff.create_file_if_not_exists(table_names_file)
def delete_item():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    selected_item = listbox.get(tk.ACTIVE)  # Lấy giá trị được chọn
    print(selected_item)
    cursor.execute(f"DROP TABLE IF EXISTS {selected_item}")
    connection.commit()
    connection.close()
    # Xóa dữ liệu từ mảng fields_2d và texts_2d
    del fields_2d[table_names.index(selected_item)]
    del texts_2d[table_names.index(selected_item)]
    # Cập nhật danh sách table_names
    table_names.remove(selected_item)
    if len(table_names) == 1 and table_names[0] == '':
        del table_names[0]
    ff.overwrite_array2d_to_txt_file(fields_2d, 'fields_2d.txt')
    ff.overwrite_array1d_to_txt_file(table_names, 'table_names.txt')
    ff.overwrite_array2d_to_txt_file(texts_2d, 'texts_2d.txt')
    tk.messagebox.showinfo("Thông báo", f"Đã xóa bảng: {selected_item}")
    update_listbox()
    dialog.deiconify()
def update_listbox():
    listbox.delete(0, tk.END)
    for item in table_names:
        listbox.insert(tk.END, item)

def handle_selection():
    selected_item = listbox.get(tk.ACTIVE)  # Lấy giá trị được chọn
    if selected_item:
        global table_name
        table_name = selected_item
        tk.messagebox.showinfo("Thông báo", f"Giá trị đã chọn: {table_name}")
        dialog.destroy()  # Đóng cửa sổ
    else:
        tk.messagebox.showwarning("Cảnh báo", "Vui lòng chọn một giá trị")
    fui.display_data(table_name, texts_2d[table_names.index(table_name)],table, root, scrollbar_y,scrollbar_x, screen_width, screen_height)
def show_options():
    global listbox  # Đặt listbox là biến toàn cục để có thể truy cập trong hàm khác
    global dialog  # Đặt dialog là biến toàn cục để có thể truy cập trong hàm khác
    dialog = tk.Toplevel(root)

    # Tạo Frame để chứa Listbox và đặt viền cho Frame
    frame = tk.Frame(dialog, borderwidth=5, relief=tk.GROOVE)
    frame.pack()

    # Tạo danh sách (Listbox) để hiển thị các phần tử trong mảng table_names
    listbox = tk.Listbox(frame)
    listbox.pack()

    # Thêm các phần tử từ mảng table_names vào danh sách
    for item in table_names:
        listbox.insert(tk.END, item)

    # Tạo nút bấm để chọn giá trị
    select_button = tk.Button(dialog, text="Chọn", command=handle_selection)
    select_button.pack()
    delete_button = tk.Button(dialog, text="Xóa", command=delete_item)
    delete_button.pack()
    display_button = tk.Button(root, text='DISPLAY DATA', command=lambda: fui.display_data(table_name, texts_2d[table_names.index(table_name)],table, root, scrollbar_y,scrollbar_x, screen_width, screen_height))
    display_button.place(x=250, y=10, width=120, height=30)

    
fields_2d = ff.read_array_from_txt_file(fields_2d_file)
texts_2d = ff.read_array_from_txt_file(texts_2d_file)
table_names = ff.read_array_from_txt_file(table_names_file)
fields = []
texts = []
table_name = 'database'
# Kết nối tới database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
columns = ['ID'] #Sau khi bỏ dấu và dấu cách, thêm cột ID
# Tạo giao diện sử dụng Tkinter
root = tk.Tk()
root.title('Table')
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
# Thiết lập kích thước cửa sổ chỉnh sửa
root.geometry(f"{screen_width}x{screen_height}")
# Tạo khung cuộn ngang
scrollbar_x = ttk.Scrollbar(root, orient=tk.HORIZONTAL)
# Tạo khung cuộn dọc
scrollbar_y = ttk.Scrollbar(root, orient=tk.VERTICAL)
# Tạo bảng
table = ttk.Treeview(root)
# Thiết lập liên kết cho thanh trượt ngang và dọc
scrollbar_x.config(command=table.xview)
scrollbar_y.config(command=table.yview)
# Hiển thị khung cuộn và bảng
scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
table.place(x=10, y=50, width=screen_width-40, height=screen_height-150)
###########################################
create_button = tk.Button(root, text='CREATE NEW FORM', command= lambda: fui.create_form(fields_2d, texts_2d, table_names, table, root, scrollbar_y, scrollbar_x, screen_height, screen_width))
create_button.place(x=380, y=10, width=130, height=30)
test_button = tk.Button(root, text='TEST CODE', command=lambda: fui.test_code(table_name, fields_2d, table_names, texts_2d))
test_button.place(x=520, y=10, width=100, height=30)
button = tk.Button(root, text="CHOOSE TABLE", command=show_options)
button.place(x=630, y=10, width=100, height=30)
print(fsql.get_table_names())
root.mainloop()