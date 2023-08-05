#coding=utf8
import json
import requests
import time
import sys, getopt
import os

def similated_login():
    UserAgent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    # cookie = "_qddaz=QD.ck0ido.86ez64.jxvb8ajg; pgv_pvi=8434611200; pi=2978375626464058%3bp2978375626464058%3b%e8%82%a1%e5%8f%8bm6gwJP%3bUs6d6O7HAegppyItRw%2bv7hsPSDVXjyUuXpqD1W8eGIGY24%2baRxPGCSl1NusJefvxnF8tYa3%2frPlWvylPC6XDniSgovCfZXmPbmFg7POm84YCcy5%2fPu74oR977R4ucounwvSI%2fFkTepe6COLFP0rUbLY6XN85Cb1HxnDe0Hc1BFifyG%2fosUd%2bkJu9IXNL4nTLbep%2bRTJf%3bfpdYVLJaQWGlokPvA3uEXrHR2H9i%2bUMI5OkczJYrSOm9BuQnUA6n8XoXxo8Bs08WTMI8jE8Oky4iFzMsAILVcOtcEwfdkrOeX3iVWu1xH0wQqQmgdxIIEvliwRTAal6ceTPuofz%2bp00CUdzIdcpiPouPB5kk1w%3d%3d; uidal=2978375626464058%e8%82%a1%e5%8f%8bm6gwJP; st_pvi=69229702233497; st_sp=2019-02-21%2019%3A00%3A09; st_inirUrl=https%3A%2F%2Fwww.baidu.com%2Flink; qgqp_b_id=c849b0095aea67ea70c18fe13eabde7d; __RequestVerificationToken=0GNbPrEHeH6iqIeMyUvLJwrqZijIgh94VMR8JbEjbuQhKxNYPIVOmMU8jaJew4pK3IitM7uMxHWi2fdEBF363xs3A3M1; .ASPXAUTH=471338D3D3913CF0C3DFC7A1C548BF8EEFBD0A007F56D58CAD89DC8F0709369DBEB0492345CA7FF35169B0B0CF0A17292D8ADCCEF64F7A83CFABCED1ADF634D614D6ACFAF57DF95F00D91BC39A0B51F2B64D5A562CE88B89F25D5A1BE5E70DFCE1D96D7692DD51B87188086A47611DD9AC92D171084DC154641B2B30B1DD2624ED261D4141865236DB25DD5EE2046620F6E082D8773B85AF7FA405340A6D67A227A33F6A769D47BDB9871171811350922DCD49E033EBAB0C0A74CB1596495DE8689D6D3F8293E5A57406E7E539E9192792E16B408987FBDC2D58E25EA92259BA3ECC4714FBDAB16452061BD5A41AEC30CF6D2514A58E56CBBBA1F25E60CF79B091B3F75EA8536E6C6581ABD616DAC8503FE8F43793416169A18C42B7F769E8AADAF727E283115C5C0A9AC0FC1B04F3CD950264DECEB3CDF50B8B01C21394415C81F48E58D5CE5B12AB293814E2A14E25B78648403CF3CCF0B463D761B7CEB17904D07F71096002C83319841E256B4B991213FB3206C42DB63FC0CC561074AC89AD68201FA6D5905144A6D1D467B76246C4C8D110A9BC99E95C13D9760604B430406222AE694B1C6D344A9C60EA3EE6C1E83469F526723FDF38896BE6762E46138524E019A8BCD21B1F10F151BFEE09B602EC40EDAA2F38AAE72A58DBC71411A8167378EA6052B551EA0C87CD69498E9A4AFDF32C9736F57C8F1DD46C6AA8019E5738EF4C4A0BF49190E5F342ABC0C7DA1F9946763B3239C0AA2D27ADE6D3DEECDDA054BB583A6E5CE0DA0A2985AF107F625B860BDED01788E11A72283E56657A174F15EF3F6CD22CAFC127B1799C351C2E01C7112CB83E1DBF1FA4CBD16F38CF7A4432D9DBB0C54ED604F9AEBE3D84694379A7AA91AED1FF4B4C634EF6FFDB1075EEA5F2E8C152118798662720CD7D0324D8244CEBB3846BF657BDD6F00C14202F50A352ED16FB0E584D018D23510FEE19DBDB7B83819B9577668E867B714523BEC9D7311BE7908038E5757675123F5A515290E71355DBCE14469627F710D25FDE9CFE8F2EDF60F8896538BD7D1917542AE677B5B636E3369964489EDB5777898B97D64518A2EF6BEC76E9CED93044A892A90265A3CC516B482AE8574EF0A85EEB0FF5C851F1166921613B54EC7F0E7480CC36C9A408611E8DB61EBD10B967ECA1F0B8D2F291497990159D6AB7EA77D8046F2DB393198533C95B98DE6C700FC6AA133F8072364C4E786054B6F6E31BA71FD9B35FF0C28A04C5A1B85D65B95CB1E32047458F0A260C87DEF423DD828820442CFA581ACB473138236F305E5330395CE7400D568D86ABB164DCB8B8A1D83CAFC56F58176C9111BB14C784561CC44E7A828D19BC74C9CA402CC72F45BD806B0CBEC345B5FCF0890F53C8681D00E980B24387996DDAE688E1D64809E87C6FBBD548F81F720726E6780DF59E0305BA0596568B1F345654679C5501745AD128CF3809C4E9FDBE01407426AC92E2E1D32B9B80819D7856983B52078BE1FF8859974AD483EC3DB6DC814BD0A4A318520D26018D78AD9ED90CCAB9EB2A049D11F24698FCE8529FBD854DA467BC80C0E694F1D713CB8C83337FA9F7F80DAE3269EBF02E3FF1CFB313AD6DBA8AC0E7406CBA53F32E1A9F7F9118CD74CBD455D61FA0A2F7D12C7B153735701D02B4FD66902CFEF9338D050258DC7045DA9B2FD8653E8137379DC2D6F18F86D5B064D8C6060C7A0C7502C844375CBF7E768C86C3B496CEBE10821726684673EDD30297918364AF5528D6758DBF33F62B456F5BA441E483E17567A5D6DF8FFCEEDBB667DA1131318DA9F0CA17A9F670577A8F64FB3E00871BB045D804EF3123D29B3F82A029C8AE57B3920D; ct=nOJuEE_ZtrNQs1Oj2nSUAbiPZutF4NZ2X75BR28kmZg5IpwKzvSftJiQCMe-8KFZg-RswbQKE0HZJAT0owhv-RlRhf7npopJUzs-o1aPY9MKe77EPAbMgjUYo98sYUWawGqGq-0t9p5iFaZQ54dv6fPidwYnCpauzjNdJKIbe5g; ut=FobyicMgeV5muwwBvHCVN4wxjlqkU47ReItRXftqa-WslykhA_JcsneuX4lc0KPEFozPs1qbkv0GLi9PXz7E322URNtbFQAQGSGnyM88XUDsxe8iaoI9cXhZme5eRwnQCFfOIAZKfJv-OW1joX15YIpsHisKTjazMsoK1qPItJRlyDNtg72gk5QqijZhWkxCaqUdwnjMcqHeWyzFz6yx7kdOeX6KUEMSUK4gelsNT2O26JI4XPJiiQUHG0WJ0GWkuO4KLYX4-gnksf9Gq4v0BFVgeBD_UrMytG2Iz8UXrbY"
    cookie = "_qddaz=QD.ck0ido.86ez64.jxvb8ajg; pgv_pvi=8434611200; pi=2978375626464058%3bp2978375626464058%3b%e8%82%a1%e5%8f%8bm6gwJP%3bUs6d6O7HAegppyItRw%2bv7hsPSDVXjyUuXpqD1W8eGIGY24%2baRxPGCSl1NusJefvxnF8tYa3%2frPlWvylPC6XDniSgovCfZXmPbmFg7POm84YCcy5%2fPu74oR977R4ucounwvSI%2fFkTepe6COLFP0rUbLY6XN85Cb1HxnDe0Hc1BFifyG%2fosUd%2bkJu9IXNL4nTLbep%2bRTJf%3bfpdYVLJaQWGlokPvA3uEXrHR2H9i%2bUMI5OkczJYrSOm9BuQnUA6n8XoXxo8Bs08WTMI8jE8Oky4iFzMsAILVcOtcEwfdkrOeX3iVWu1xH0wQqQmgdxIIEvliwRTAal6ceTPuofz%2bp00CUdzIdcpiPouPB5kk1w%3d%3d; uidal=2978375626464058%e8%82%a1%e5%8f%8bm6gwJP; st_pvi=69229702233497; st_sp=2019-02-21%2019%3A00%3A09; st_inirUrl=https%3A%2F%2Fwww.baidu.com%2Flink; qgqp_b_id=c849b0095aea67ea70c18fe13eabde7d; __RequestVerificationToken=Fe0hxnPiU8Kg1P2VkLSo5MbFhvg5pKIYkM45qtcq2h3VQVT_EEAIw8GJh6t29AoqKkfc5_SQ4oPvulenOMBF-mChnn81; .ASPXAUTH=C0A412DD757496CF8731A17AEC31726102C0B8F93C32BB230A956657CB16A94C5283969A8B2360B91B021D437A822F384B2FD93B87A95D97C3D30232776680392003E2C130B177ADBDFEF304F1D55692E513A98B378C95626B207B837250FA2545F178F9D9E5B6EA284569C0A92960063CBD3BA369AA743C8015C4D7BB5F8AC0BB03E98541F1503294A35E43AFED5147FA3686B855502A7FDDAC1745C01F6C9C96A00CF7A522B546A61F6513887E017B104B3B25FAC0DF44F0DA38B79CE0635CEB9B7F86E16DF0471A0E619019BE4DA2A82D6B1ABF18B002CD75B59C815E1B14660505259123306D20092D8DAFA300219294B9FC83053A015AFCB0B4855A4E093931AAE86F194AAF98424BE729727F545C6BFC241ADA457DEB0FA7726E549FB07E0D1163A8943F71AD979AC93564C18AC6CAA0086A2A3D408692240F7D6CB2CF166D9F490D9C21F95CCF653D4FEAD7D4FE89FB9E2267F7C6D63EA7549BD3F1E873F222AEAC7F12F37A65F585BC31323CDB66156BC9458C0D151A9F3724A51B160D6C53341BCAFB27B7DDA75DA70F36C851BDE7454F2BACFE87317B043AF2BBC7C52AD9C4CDE65494B955E58267FDB20A31E038FBD934A855436738F21C09F8B5AD3DAF6E0BDD22DE2CAF1D7B5271DFF1E673658D022BBD28DFC71171C55329738047F471EF698915EC6BA233E3EAD2861C3E89ACD3023266130D7AEB9A81221A671A4DB901BA3A5302BBF0B0E097CBFAB38380822F5060D5552B6CDA018D260A36CCA5F3F52A26369A743F772A9E48BF8211472A5C46ED1C42E0A4297503D4A4798D5A4B43D8C03BA1831C22F52F5BAA5D4B802CF42474CDBF3D02B0DCA05475EF440E83C2FA02BC7D952B420504937289D38AC19CCA14CB2F323CF1104FA21D73AA3932BCAA025A914CCE9EF14679F52625B80D61F391770BEE49EF0A2AF60DBEA674EC951AED2EE9D42F59E8FF4B4E730B5BCC24B126C718917D7D005243182170B2A3B694392487C2CE74CF066E3ACDD8AD37306F7C64F75CC62C7C8C5619497674E7D846839B6B61F5BEBA8BF3C1C6B31569ED9A39B90499FDE583FE7C78ADF4121BB272DF87C37F6A99B1853F7FB91984D5E5C8C52D518E87D7AAFB801A864530B7F0D8CD964C96BD63ED664EBC896643FA768B552D111B13144D4796DC11CFE020B62E6CF6E979E8164D568636DB4CD2230AB49191D1167BEAD35C8AD396D091492367717E7E1E8B598905BC8C85E925CCEEE357450B25D54E51A18732B49BAA8CF43BDAED59D3DCCECC3DABA01F4269244FF5DD40224EC280A246C1570CBCBFC00F4074A95210DF5AAEB9A593072EC1A0FFADD002E7A7545C27D9BC2E33BDEE546861C98244D536F5885F2FB09D616458D26F1049233B9572370BF0A024D9AD41159E319EB21833C785E51DC9D33AD89E596EF182B127D6ABCE7E2A5E578D017D0E2E0858F739E62FED40D41392DD067FABB60CF2CBA5D7DCE509BB20F03133047317EFAB3F265FE676AA4B2C9249E31B961100C18BC8FC9D098F607F96806050E101A21863D1FA981EF62BCA22ED10EC0C46DA5EF9E3A7D0F983A2C62AFBCC9E5D37A04989209D4290F818F38C4B73F326F030FC0FD4B026A753ACCEA81C5479167B4017780427AF1DC2C86F4D084D961C9EFD3B0364F4C850B491FBA9B1E91D6173166A21CB252E6A2539BA49A93E1FACBBAA7CF2D12F261FC01AC0FFCDA0BFC7C0965819C306A87F833F5FB9E36DA10A3C522662C29E4C168017149AECC19579AA13BA344A630B2B1E58AE762F1E10B3A23A492C07404BE1C1D65DDF6CEF82BD967F6093F687A3F7DB57AE3F727497CDE4D9C458F812A7999041CE6C38E81D; ct=y7VZLfs4q1ve0xHKSNNges3Dpm4LaL052cXtHjovcODe9Cz4fCnKJPRZZsNw0NVzpBAcTk9f46zgb6LvHicFlyFFiiVdrOEFPZOTAoSPnqktpPg8N3KNAYTA4jh3SiLz5zMTd7pNxyA4DIMT1Ba5XoBZtZ8H66ePtWxZJLozd9U; ut=FobyicMgeV60R-wNFHdtrOWZxbCnaEUxQ-g_R7oA6SxI14Xv3mTtOdPRvmzCtdZOOVUyAm8YgXJh0xJk01qzHbKOPSNilfYBq7ItjaRqRHBg3fmfiqcWNOXHMh9pFN-1fiSAPe_-f4CySOEj7mwYIf9jFPgDzN7psOHOjra_ortASn6dnx-x0mxNvyHWfDZp23IZEtj65tB9XhQlQE1DRpVgahM4aSq8TOcjVuMkZO-srA2FGduNbORcC9lyq5pOCV_9ckEFiKoARVvQuNNiG5V8tmtrR-ag"
    header = {
        "Referer": "http://quantapi.eastmoney.com/Cmd/ChoiceSerialSection?from=web",
        'User-Agent': UserAgent,
        "Cookie": cookie
    }
    return header

def get_url(base_url, str):
    final_url = base_url+str
    return final_url

def get_url_content_json(url):
    try:
        header = similated_login()
        content = requests.get(url, headers=header).content
    except Exception as e:
        for i in range(10):
            time.sleep(10)
            try:
                print("**************")
                print("auto retry N0."+str(i+1))
                print("**************")
                header = similated_login()
                content = requests.get(url, headers=header).content
                break
            except Exception as e:
                continue
    return json.loads(content)

def find_all_upper_nodes(content_list,sub_content):
    resault_str = ""
    resault_str += sub_content.split("\t")[0]+"\t"
    start_index = int(sub_content.split("\t")[0])
    node_list=[]
    while(start_index!=-1):
        for item in content_list:
            if len(item.split("\t"))==1:
                continue
            if int(item.split("\t")[0])==start_index:
                node_list.append(item.split("\t")[1])
                start_index = int(item.split("\t")[2])
                break
    node_list=node_list[::-1]
    final_node_route = "-".join(node_list)
    resault_str += final_node_route+"\n"
    return resault_str

def file_comparation(filename, new_content):
    f = open(filename,"r", encoding="utf8")
    old_content = f.readlines()
    f.close()

    old_not_in_new = []
    new_not_in_old = []
    for item in old_content:
        if item not in new_content:
            if len(item.split("\t"))==1:
                old_not_in_new.append(item)
            else:
                str_all_upper_nodes = find_all_upper_nodes(old_content,item)
                old_not_in_new.append(str_all_upper_nodes)
    for item in new_content:
        if item not in old_content:
            if len(item.split("\t"))==1:
                new_not_in_old.append(item)
            else:
                str_all_upper_nodes = find_all_upper_nodes(new_content,item)
                new_not_in_old.append(str_all_upper_nodes)
    if len(old_not_in_new)==0 and len(new_not_in_old)==0:
        return False
    if len(old_not_in_new) != 0:
        base_filename = filename.split(".")[0]
        compare_filename = base_filename + "_old_not_in_new.txt"
        f = open(compare_filename,"w", encoding="utf8")
        f.writelines(old_not_in_new)
        f.close()
    if len(new_not_in_old) != 0:
        base_filename = filename.split(".")[0]
        compare_filename = base_filename + "_new_not_in_old.txt"
        f = open(compare_filename,"w", encoding="utf8")
        f.writelines(new_not_in_old)
        f.close()
    return True

def store_content_in_txt_file(default_filename,content,default_firstline="req_fn_tree_nodes_start",**kwargs):

    for i in range(len(content)):
        content[i] = content[i].split("\n")[0]+(8-len(content[i].split("\n")[0].split("\t")))*"\t"+"\n"

    if "filename" in kwargs:
        filename = kwargs["filename"]
        if len(filename) == 0:
            filename = default_filename
    else:
        filename = default_filename
    filename += ".txt"

    if "first_line" in kwargs:
        first_line_str = kwargs["first_line"]
        if len(first_line_str) == 0:
            first_line_str = default_firstline
    else:
        first_line_str = default_firstline
    first_line_str += "\n"
    content.insert(0,first_line_str)

    weather_new = False
    if os.path.exists(filename):
        weather_new = file_comparation(filename,content)
    if weather_new:
        print("*************")
        print("data updated")
        print("*************")
        name_of_old_file = filename.split(".")[0]+"_old.txt"
        try:
            os.rename(filename, name_of_old_file)
        except Exception as e:
            os.remove(name_of_old_file)
            os.rename(filename, name_of_old_file)
    else:
        print("*************")
        print("no data updated")
        print("*************")

    f = open(filename,"w", encoding="utf8")
    f.writelines(content)
    f.close()

def filter_end_tab(data_str):
    return "".join(data_str.split("\t"))

def filter_all_spaces(data_str):
    result_str = filter_end_tab(data_str)
    result_str = "".join(result_str.split("\xa0"))
    return result_str

def help_file():
    help_str = """
    usage: python [py_filename] -f filename -t title
    -f  : filename of the file to be stored
    -t  : the first line of the file to be stored
    -l  : the local path of file to be stored, remember, this should be the absolute path and the filename should not be contained
    """
    return help_str

def process_system_parameter(argv):
    filename = ''
    title = ''
    local_path = ""
    try:
        opts, args = getopt.getopt(argv, "hf:t:l:", ["help", "filename=", "title=", "localpath="])
    except getopt.GetoptError:
        print("error way to give parameters")
        print(help_file())
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("'-h'", "--help"):
            print(help_file())
            sys.exit()
        elif opt in ("-f", "--filename"):
            filename = arg
        elif opt in ("-t", "--title"):
            title = arg
        elif opt in ("-l", "--localpath"):
            local_path = arg
    return {"filename": filename, "firstline": title, "local_path":local_path}

