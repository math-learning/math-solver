class PrintUtils:

    def solution(self, input, history):
        print( "Partiendo de: ")
        print (input)
        for item in history:
            print("aplico " + item.theorem_applied.name + " y obtengo como resultado:")
            print(item.expression)