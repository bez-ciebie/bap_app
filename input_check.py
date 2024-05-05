#输入格式处理  遍历一遍 判断类型 前面是float:.2f  后面是int
###需求：输入变量中的供氢溶剂、催化剂这些是定性变量，应该是作为一个文本输入，在后端将其转化为数值型变量，然后预测
def input_check_all(Mad, Ad, Vdaf, Cin, Hin, Nin, Sin, Oin, Tin, Pin, Time, Addition, nS, Sc, Solvent_type, Catalyst, Atmosphere) -> list | None:
    li = []
    ##读取所有的输入到列表中
    l= locals()
    for idx,key in enumerate(l):
        li.append(l[key])
        if idx == 16:
            break
    #print(li)

    #所有数值输入是否不为0
    all_not_zero = all(float(item) != 0.00 for item in li[0:16])

    if all_not_zero:
        float_list = [float(item) for item in li]
        return float_list
    else:
        return None
    

    