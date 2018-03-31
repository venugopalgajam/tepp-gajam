import datetime as dt

table="""<table class="table table-bordered table-hover table-striped table-condensed" id={{id_}}>{{thead}}{{tbody}}</table>"""
th="""<th class="text-center {{class_}}">{{data}}</th>"""
td="""<td class="text-center {{class_}}">{{data}}</td>"""
def render_table( id_, table_head_list, table_body_list, table_hclass_list=None, table_bclass_list=None):
    assert ((table_hclass_list is None) or len(table_head_list) == len(table_hclass_list))
    assert ((table_bclass_list is None) or len(table_body_list[0]) == len(table_bclass_list))
    # print(len(table_head_list),len(table_body_list))
    if len(table_body_list) > 0:
        assert (len(table_head_list) == len(table_body_list[0]))
    
    table_html = str(table).replace('{{id_}}',id_)
    
    thead =""
    for idx in range(len(table_head_list)):
        cell = str(th).replace('{{data}}',str(table_head_list[idx]))
        cell = cell.replace('{{class_}}','' if table_hclass_list==None else table_hclass_list[idx])
        thead += cell
    thead = '<thead>'+str(th).replace('{{data}}','S.No.').replace('{{class_}}','')+thead+'</thead>'
    table_html=table_html.replace('{{thead}}',thead)

    tbody = ""
    for row in range(len(table_body_list)):
        tr =""
        for col in range(len(table_body_list[row])):
            cell = str(td).replace('{{data}}',str(table_body_list[row][col]))
            cell = cell.replace('{{class_}}','' if table_bclass_list==None else table_bclass_list[col])
            tr += cell
        tr = '<tr>'+str(td).replace('{{data}}','').replace('{{class_}}','')+tr+'</tr>'
        tbody+=tr
    tbody ='<tbody>'+tbody+'</tbody>'
    table_html=table_html.replace('{{tbody}}',tbody)

    return table_html
