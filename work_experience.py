import string


class WorkExperience():
    def __init__(self, text):
        self.content = [y for y in (x.strip() for x in text.splitlines()) if y]
        self.parse()

    def checkLine(self, word, value, content, line):
        if word in content.lower():
            value = self.addValue(value, line)
        return value

    def addValue(self, value, line):
        value[line] = value.get(line, 0) + 1
        return value

    def dict_List(self, dict_, content):
        new = [(key, value) for key, value in dict_.items() if dict_[key] == max(dict_.values())]
        return [(x[0], content[x[0]]) for x in sorted(new)]

    def get_name(self):
        names = []
        for each in self.name:
            if each[0] not in self.headings:
                each = each[1].replace('Name', "")
                if each[0] not in string.letters:
                    each = each[1:]
                names.append(each.strip())
            else:
                index = self.headings[self.headings.index(each[0]) + 1]
                names.append("\n".join(self.content[each[0] + 1:index]))
        if len(names) == 1:
            return names[0]
        else:
            return names

    def get_work(self):
        experience = []
        for each in self.work:
            index = self.headings[self.headings.index(each[0]) + 1]
            experience.append("\n".join(self.content[each[0] + 1:index]))
        if len(experience) == 1:
            return experience[0]
        else:
            return experience

    def parse(self):
        name = dict()
        work_experience = dict()
        isHeading = dict()
        for line_num in range(len(self.content)):
            for checkName in ["name", ":"]:
                name.update(self.checkLine(checkName, name, self.content[line_num], line_num))
            for checkWork in ["work", "experience", "work experience"]:
                work_experience.update(self.checkLine(checkWork, work_experience, self.content[line_num], line_num))
            if line_num != len(self.content) - 1:
                if len(self.content[line_num + 1]) > len(self.content[line_num]):
                    isHeading.update(self.addValue(isHeading, line_num))
            if line_num > 0:
                if self.content[line_num - 1] == "":
                    isHeading.update(self.addValue(isHeading, line_num))
            if len(self.content[line_num]) == len(self.content[line_num].lstrip()):
                isHeading.update(self.addValue(isHeading, line_num))
            if self.content[line_num] == "":
                isHeading[line_num] = isHeading.get(line_num, 0) - 1

        self.name = self.dict_List(name, self.content)
        self.work = self.dict_List(work_experience, self.content)
        self.headings = self.dict_List(isHeading, self.content)
        self.headings = [x[0] for x in self.headings]

if __name__ == '__main__':
    resume = Resume(filename = 'sampleresume.txt')
    WorkExperience().get_work()