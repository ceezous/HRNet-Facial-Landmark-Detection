import sqlite3

def act1():
    # create
    conn = sqlite3.connect("nme.db")
    c = conn.cursor()
    c.execute(
        '''
            CREATE TABLE nme(
                name text,
                type char(3),
                nme real
            )
        '''
    )
    conn.commit()
    conn.close

def act2():
    # check
    conn = sqlite3.connect("nme.db")
    c = conn.cursor()
    cursor = c.execute(
        '''
            SELECT *
            FROM nme
        '''
    )
    counter = 0
    for row in cursor:
        counter += 1
    print(counter)
    conn.commit()
    conn.close

def act3():
    # delete
    conn = sqlite3.connect("nme.db")
    c = conn.cursor()

    print("请输入yes以删除数据:")
    judge = input()
    if judge != "yes":
        return

    cursor = c.execute(
        '''
            DELETE FROM nme 
        '''
    )
    conn.commit()
    conn.close

def act4():
    # check pre 10
    conn = sqlite3.connect("nme.db")
    c = conn.cursor()

    cursor = c.execute(
        '''
            SELECT *
            FROM nme 
        '''
    )
    counter = 5
    for row in cursor:
        if counter <= 0:
            break
        counter -= 1
        print(row)

    conn.commit()
    conn.close

def act5():
    # 选出degrade训练出但效果较差的图片
    conn = sqlite3.connect("nme.db")
    c = conn.cursor()

    cursor = c.execute(
        '''
            SELECT *
            FROM nme a, nme b
            WHERE a.name = b.name and a.type = "ori" and b.type = "dgr" and a.nme < b.nme
        '''
    )
    counter = 0
    for row in cursor:
        print(row)
        counter += 1
    print("数量：", counter)

    judge = input("是否保存在./visual/bad_image中？y/n:")
    if judge == 'y':
        cursor = c.execute(
            '''
                SELECT a.name
                FROM nme a, nme b
                WHERE a.name = b.name and a.type = "ori" and b.type = "dgr" and a.nme < b.nme
            '''
        )
        import os
        for row in cursor:
            
            old_path = row[0]
            new_path = "./visual/bad_image/" + old_path[22:]
            print(f"from {old_path} to {new_path}")
            os.system(f"cp {old_path} {new_path}")

            old_path_bk = old_path
            new_path_bk = new_path

            old_path = old_path_bk[:-10] + "_origin.jpg"
            new_path = new_path_bk[:-10] + "_origin.jpg"
            print(f"from {old_path} to {new_path}")
            os.system(f"cp {old_path} {new_path}")

            old_path = old_path_bk[:-10] + "_degrade.jpg"
            new_path = new_path_bk[:-10] + "_degrade.jpg"
            print(f"from {old_path} to {new_path}")
            os.system(f"cp {old_path} {new_path}")

    conn.commit()
    conn.close

if __name__ == "__main__":
    while 1:
        print("请输入你想要进行的操作：")
        print("1.创建数据库")
        print("2.查看数据量")
        print("3.清空数据库")
        print("4.查看数据库前5项")
        print("5.选出degrade训练出但效果较差的图片")
        number = input()
        exec("act" + number + "()")
