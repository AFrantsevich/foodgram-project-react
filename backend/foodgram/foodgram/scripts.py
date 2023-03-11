def delete_dub(list_product):
    j = 0
    try:
        while True:
            obr_ing = list_product[j][0].lower()
            obr_measure = list_product[j][2].lower()
            m = 0+j
            for i in range(1, len(list_product)):
                m += 1
                if (list_product[m][0].lower() == obr_ing
                        and list_product[m][2].lower() == obr_measure):
                    list_product[j][1] += list_product[m][1]
                    del (list_product[m])
                    m = 0+j
            j += 1
    except IndexError:
        return list_product
