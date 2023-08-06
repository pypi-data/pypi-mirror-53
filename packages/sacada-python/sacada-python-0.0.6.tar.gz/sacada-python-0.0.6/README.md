# sacada-python

A biblioteca em Python do SACADA permite que sejam desenvolvidas aplicações científicas de maneira amigável e abstraída. 

---

# Instalação

A biblioteca, junto com o comando `sacada` pode ser instalada globalmente com o comando
```
sudo pip3 install -U sacada-python
```

Caso deseje instalar apenas localmente, ou se não tiver acesso ao sudo, instale utilizando 
```
pip3 install --user -U sacada-python
```
Tome cuidado que, neste caso, o comando `sacada` ficará disponível apenas em `~/.local/bin`, que deverá estar no seu `PATH`.

---

# Uso

## Biblioteca

[TODO] Escrever códigos de [exemplo.](/Exemplos)

```python
from sacada import SACADA

s = SACADA("/dev/ttyACM0")

# Imprime a tensão do canal A0 na tela
print(s.readVoltage("A0"))
```

## Comando

O comando `sacada` permite a interface com a placa via terminal. Ele faz uso de uma interface serial, então é importante que você tenha as permissões corretas para acesso. Caso você esteja tendo erros de permissão, tente se colocar no grupo `dialout` utilizando o comando `sudo usermod -aG dialout [seu usuario]` e relogue no seu computador.

Para testar a comunicação, você pode utilizar o comando `sacada show`, que deve retornar a string de identificação da placa que você está utilizando. Para especificar uma porta, você pode utilizar o parâmetro `--port [sua porta]`. Por padrão, a porta utilizada é a `/dev/ttyACM0`. É importante frisar que a SACADA possui **duas** portas seriais, e que a utilizada para comunicação é **sempre a de número menor**.

**Exemplos:**
```
[tropos@cta-001 ~]$ sacada show
blazing.design/UFRGS,SACADA Mini,0,rev1
```

```
[tropos@cta-001 ~]$ sacada --port /dev/ttyACM123 show
blazing.design/UFRGS,SACADA Mini,0,rev1
```

**O parâmetro --port deve ser sempre o primeiro do comando**

Para medir um canal único, você pode utilizar o comando `read`:

**Exemplo:**
```
[tropos@cta-001 ~]$ sacada read A0
3.29312515258789
```

Caso você deseje monitorar um canal continuamente, pode utilizar o comando `monitor`. Você também pode especificar um arquivo para salvar os dados utilizando o parâmetro `--save`. O intervalo de amostragem pode ser especificado (em milisegundos) com o parâmetro `--interval`.

**Exemplos:**
```
# Monitora o canal A0 com o intervalo padrão de 1000ms

[tropos@cta-001 ~]$ sacada monitor A0
3.29312515258789
3.29187512397766
3.29175019264221
...
```

```
# Monitora o canal A0 com intervalo de 100ms

[tropos@cta-001 ~]$ sacada monitor A0 --interval 100
3.29287505149841
3.28575015068054
3.28275012969971
...
```

```
# Salva no arquivo ~/logs/out.log as amostras lidas

[tropos@cta-001 ~]$ sacada monitor A0 --save ~/logs/out.log
3.29275012016296
3.29187512397766
3.29212522506714
...
```

**Os valores lidos e monitorados sempre serão dados em Volts**

---

# Licença

Este programa é um software livre; você pode redistribuí-lo e/ou
modificá-lo sob os termos da Licença Pública Geral GNU como publicada
pela Free Software Foundation; na versão 3 da Licença, ou
(a seu critério) qualquer versão posterior.

Este programa é distribuído na esperança de que possa ser útil,
mas SEM NENHUMA GARANTIA; sem uma garantia implícita de ADEQUAÇÃO
a qualquer MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a
Licença Pública Geral GNU para mais detalhes.

Uma cópia da licença (em inglês) está disponível no arquivo [LICENSE](/LICENSE).

---

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

A copy of this license is provided in the [LICENSE](/LICENSE) file.

---

Copyright 2019 Pedro Henrique Capp Kopper.
