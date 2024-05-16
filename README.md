Este projeto é um sistema bancário simples desenvolvido para fins acadêmicos. Ele permite que um usuário único execute operações bancárias básicas como depósitos, saques e a visualização de um extrato. O sistema não exige detalhes como agência ou número de conta, simplificando o modelo para uso educacional.

Funcionalidades
Depósitos: O usuário pode depositar valores positivos no sistema. Cada depósito é adicionado ao saldo total e registrado no extrato.
Saques: Limitados a três operações diárias com um valor máximo de R$500 por saque. Caso o saldo não seja suficiente ou o limite diário seja excedido, a operação é negada.

Extrato: Mostra todas as transações realizadas, incluindo depósitos e saques, com valores em formato monetário (R$).
Considerações Técnicas
As operações são registradas numa lista de transações, facilitando o rastreamento do histórico.
O saldo é atualizado a cada operação e é apresentado em formato monetário usando a localidade pt_BR.
Este sistema é ideal para estudantes que desejam entender os conceitos básicos de operações bancárias e a manipulação de estados em programas.
