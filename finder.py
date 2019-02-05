class Finder:
    def findtheid(self, sku):
        for i in spd:
            if(i["sku"]==sku):
                print("Id of " + sku + " = "+i["id"])
                return
        print(sku+ " not Found in .py file")
