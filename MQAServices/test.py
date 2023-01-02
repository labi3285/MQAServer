import json
from django.core import signing

value = signing.dumps({"foo": "bar"})
src = signing.loads(value)

print(value)
print(src)

lob = 'Acoustic'
site = 'Merry'
productLine = 'iPhone'
project = 'D54'
part = 'Speaker'

islineexist = True

filepath = '/Users/mqa_server/Desktop/test.json'

def resolveJson(path):
    file = open(path,"rb")
    json_file = json.load(file)

    temp_lob_dict = {}
    if lob in json_file['level_content']:
        for dataDic in json_file['level_data']:
            if dataDic['lob_name'] == lob:
                temp_lob_dict = dataDic
                break

        temp_site_dict = {}
        if site in temp_lob_dict['lob_content']:
            for site_dic in temp_lob_dict['lob_data']:
                if site_dic['site_name'] == site:
                    temp_site_dict = site_dic
                    break

            temp_line_dict = {}
            if productLine in temp_site_dict['site_content']:
                for line_dic in temp_site_dict['site_data']:
                    if line_dic['line_name'] == productLine:
                        temp_line_dict = line_dic
                        break

                temp_project_dict = {}
                if project in temp_line_dict['line_content']:
                    for project_dic in temp_line_dict['line_data']:
                        if project_dic['project_name'] == project:
                            temp_project_dict = project_dic
                            break

                    if part in temp_project_dict['project_data']:
                        if islineexist is True:
                            print('产线已存在')
                        else:
                            print('产线添加成功')

                        return '产线添加成功'

                    else:
                        print('添加part')
                        change_islineexist()
                        temp_data_list = list(json_file['level_data'])
                        for dic in temp_data_list:
                            if dic['lob_name'] == lob:
                                temp_lob_list = dic['lob_data']
                                for dic1 in temp_lob_list:
                                    if dic1['site_name'] == site:
                                        temp_site_list = dic1['site_data']
                                        for dic2 in temp_site_list:
                                            if dic2['line_name'] == productLine:
                                                temp_line_list = dic2['line_data']
                                                for dic3 in temp_line_list:
                                                    if dic3['project_name'] == project:
                                                        temp_project_list = list(dic3['project_data'])
                                                        temp_project_list.append(part)
                                                        dic3['project_data'] = temp_project_list
                                                        temp_line_list[temp_line_list.index(dic3)] = dic3
                                                        temp_site_list[temp_site_list.index(dic2)]['line_data'] = temp_line_list
                                                        temp_lob_list[temp_lob_list.index(dic1)]['site_data'] = temp_site_list
                                                        temp_data_list[temp_data_list.index(dic)]['lob_data'] = temp_lob_list
                                                        json_file['level_data'] = temp_data_list
                                                        updatajsonfile(json_file)
                                                        resolveJson(filepath)

                else:
                    print('添加一个project')
                    change_islineexist()
                    temp_data_list = list(json_file['level_data'])
                    for dic in temp_data_list:
                        if dic['lob_name'] == lob:
                            temp_lob_list = dic['lob_data']
                            for dic1 in temp_lob_list:
                                if dic1['site_name'] == site:
                                    temp_site_list = dic1['site_data']
                                    for dic2 in temp_site_list:
                                        if dic2['line_name'] == productLine:
                                            temp_content_list = list(dic2['line_content'])
                                            temp_content_list.append(project)
                                            new_project_dict = {'project_name':project, 'project_data':['**Part**']}
                                            line_data_list = list(dic2['line_data'])
                                            line_data_list.append(new_project_dict)
                                            dic2['line_content'] = temp_content_list
                                            dic2['line_data'] = line_data_list
                                            temp_site_list[temp_site_list.index(dic2)] = dic2
                                            temp_lob_list[temp_lob_list.index(dic1)]['site_data'] = temp_site_list
                                            temp_data_list[temp_data_list.index(dic)]['lob_data'] = temp_lob_list
                                            json_file['level_data'] = temp_data_list
                                            updatajsonfile(json_file)
                                            resolveJson(filepath)


            else:
                print('添加一条product line')
                change_islineexist()
                temp_data_list = list(json_file['level_data'])
                for dic in temp_data_list:
                    if dic['lob_name'] == lob:
                        temp_lob_list = dic['lob_data']
                        for dic1 in temp_lob_list:
                            if dic1['site_name'] == site:
                                site_content_list = list(dic1['site_content'])
                                site_content_list.append(productLine)
                                new_line_dict = {'line_name': productLine, 'line_content': ['**Project**'], 'line_data': []}
                                site_data_list = list(dic1['site_data'])
                                site_data_list.append(new_line_dict)
                                dic1['site_content'] = site_content_list
                                dic1['site_data'] = site_data_list
                                temp_lob_list[temp_lob_list.index(dic1)] = dic1
                                (temp_data_list[temp_data_list.index(dic)])['lob_data'] = temp_lob_list
                                json_file['level_data'] = temp_data_list
                                updatajsonfile(json_file)
                                resolveJson(filepath)

        else:
            print('添加一个site')
            change_islineexist()
            temp_data_list = list(json_file['level_data'])
            for dic in temp_data_list:
                if dic['lob_name'] == lob:
                    tempcontentList = list(dic['lob_content'])
                    tempcontentList.append(site)
                    new_site_dict = {'site_name': site, 'site_content': ['**Product line**'], 'site_data': []}
                    temp_lob_data_list = list(dic['lob_data'])
                    temp_lob_data_list.append(new_site_dict)
                    lob_dict = dict(temp_data_list[temp_data_list.index(dic)])
                    lob_dict['lob_content'] = tempcontentList
                    lob_dict['lob_data'] = temp_lob_data_list
                    temp_data_list[temp_data_list.index(dic)] = lob_dict
                    json_file['level_data'] = temp_data_list
                    updatajsonfile(json_file)
                    resolveJson(filepath)

    else:
        print('添加一个lob')
        change_islineexist()
        templist = list(json_file['level_content'])
        tempstr = str(templist[0])
        if tempstr != '**LOB**':
            templist.insert(0,'**LOB**')
            templist.append(lob)
            json_file['level_content'] = templist
            temp_data_list = list(json_file['level_data'])
            new_dict = {'lob_name': lob, 'lob_content': ['**Site**'], 'lob_data': []}
            temp_data_list.append(new_dict)
            json_file['level_data'] = temp_data_list
            updatajsonfile(json_file)
            resolveJson(filepath)
        else:
            templist.append(lob)
            json_file['level_content'] = templist
            temp_data_list = list(json_file['level_data'])
            new_dict = {'lob_name': lob, 'lob_content': ['**Site**'], 'lob_data': []}
            temp_data_list.append(new_dict)
            json_file['level_data'] = temp_data_list
            updatajsonfile(json_file)
            resolveJson(filepath)

# TODO：每一层只处理对应该层的数据，添加后更新文件，调用自身进入下一层的判断

def updatajsonfile(newjson_file):
    with open(filepath, 'w', encoding='utf-8') as file1:
        json.dump(newjson_file, file1)
        file1.close()

def change_islineexist():
    global islineexist
    islineexist = False


resolveJson(filepath)



