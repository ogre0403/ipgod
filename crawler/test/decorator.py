import hashlib
import random
import string


def italic(func):
    def wrap(a, **kwargs):
        print("<a>")
        func(a, **kwargs)
        print("</a>")

    return wrap


def bold(func):
    def wrap(a):
        print("<b>")
        func(a)
        print("<b>")

    return wrap


@bold
@italic
def f(a, **kwargs):
    return print("anwser: {:5s}".format(str(a + a * a)))


class md5sum:

    def gen_res_idx(self, x):
        if x['result']['identifier'] and x['result']['distribution'] :
            datasetid = x['result']['identifier']
            for i in x['result']['distribution']:
                format = i['format']
                dURL = i['downloadURL']
                md5 = hashlib.md5()
                md5.update(str(dURL+ format).encode("utf-8"))
                resourceID = md5.hexdigest()[0:5]
                i['resourceID'] = datasetid + "_" +resourceID
            return x
        else:
            return x

    def gen_res_id(self, *args):
        md5 = hashlib.md5()
        keystr = str(args)
        md5.update(keystr.encode("utf-8"))
        return md5.hexdigest()[0:5]


if __name__ == "__main__":
    # f(10)
    # with open('test.json', "r",  encoding="UTF-8") as f:
    #     data = json.load(f)
    #
    # # m5 = md5sum().gen_res_id("A10220202", "today","csv",'http://a.b.c.d/her?gogo')
    # m5 = md5sum().gen_res_idx(data)
    # # m5 = md5sum().gen_res_id("today","csv")
    #
    # print(m5)
    # print()


    resourceID = "".join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=5))
    print(resourceID)