class Content:
    def __init__(self, aciton_row):
        self.action_type = action_row.split(',')[1]
        aciton_str = aciton_row.split(',')[-1]
        self.day = aciton_row.split(',')[0]
        self.id = aciton_row.split(',')[2]
        self.subject = aciton_row.split(',')[3]
        self.first_arg = aciton_str.split(' ')[0]
        self.args = []
        if len(aciton_str.split(' ')) > 1:
            for arg in aciton_str.split(' ')[1:]:
                self.args.append(arg)
