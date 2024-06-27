# 1) Criando a classe 'Calculadora'
class Calculadora:
    
    # 2) Criando o método 'soma'
    def soma(self, n1, n2):
        return n1 + n2

    # 3) Criando o método 'subtracao'
    def subtracao(self, n1, n2):
        return n1 - n2

    # 4) Criando o método 'multiplicacao'
    def multiplicacao(self, n1, n2):
        return n1 * n2
    
    # 4) Criando o método 'divisao'
    def divisao(self, n1, n2):
        if n2 == 0:
            # primeira forma de tratar divisão por zero
            # raise ZeroDivisionError("Divisão inválida")
            
            # segunda forma de tratar divisão por zero
            raise ValueError("Divisão inválida")
        else:
            return n1 / n2