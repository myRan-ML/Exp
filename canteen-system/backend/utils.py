from tabulate import tabulate

def print_table(rows, headers):
    if rows:
        data_list = [list(r.values()) for r in rows]
        print(tabulate(data_list, headers=headers, tablefmt='grid'))
    else:
        print("无数据可展示")