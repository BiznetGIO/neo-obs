from obs.libs.utils import  yaml_utils


def initialize(file=None):
    pass
    # obj_data = utils.file_parser(file)
    # class_property = dict(obj_data['class']['properties'])
    # class_obj_i = obj_data['class']['object']

    # c_params = ''
    # try:
    #     class_propertis = class_property['argument'];
    # except Exception as e:
    #     class_propertis = None

    # if class_propertis:
    #     for cl in class_propertis:
    #         arg_val = class_propertis[cl]['value']
    #         try:
    #             config = class_propertis[cl]['config']
    #         except Exception as e:
    #             config = None
    #         if config:
    #             if config['specified'] == False:
    #                 c_params += "'"+arg_val+"',"
    #             else:
    #                 c_params += cl+"='"+arg_val+"',"
    #         else:
    #             c_params += "'"+arg_val+"',"
    #     c_params = "("+c_params[:-1]+")"
    # else:
    #     c_params = "()"

    # class_obj = class_obj_i+c_params

    # function_name = obj_data['function']['name']
    # try:
    #     function_property = dict(obj_data['function']['parameters'])
    # except Exception as e:
    #     function_property=None

    # if function_property:
    #     fn_params = ''
    #     for fn in function_property:
    #         fn_arg_val = function_property[fn]['value']
    #         try:
    #             config_fn = class_propertis[cl]['config']
    #         except Exception as e:
    #             config_fn = None
    #         if config_fn:
    #             if config['specified'] == False:
    #                 fm_params += "'"+fn_arg_val+"',"
    #             else:
    #                 fn_params += fn+"='"+fn_arg_val+"',"
    #         else:
    #             fn_params += "'"+fn_arg_val+"',"
    #     fn_params = "("+fn_params[:-1]+")"
    # else:
    #     fn_params = "()"

    # function_name = function_name+fn_params
    # exec_function = 's3.'+function_name

    # status_exec = ''
    # print(class_obj)
    print(exec_function)
    # try:
    #    s3 = exe.command_class(class_obj)
    #    exe.command_execute(exec_function)
    # except Exception as e:
    #     status_exec = str(e)
    # else:
    #     status_exec = True

    # print("Client Exec : "+class_obj)
    # print("Function Exec : "+exec_function)
    # print("Error Execute : "+status_exec)
    # output_param = dict(obj_data['output']['parameters'])
    # for out in output_param:
    #     obj =