# qaz
这个项目是一个投料机的应用，在MQTT中发送一个“FFA0010EE”的命令，其中“FF”和“EE”是起始位和截止位，“A”是模式，“0010”代表持续时间。其中组合动作：开灯10s->开风机10s->开投料机10s（0010传的10s）->等待10s->关闭风机->等待一分钟->关闭灯。当执行time.sleep（60）时，第一次MQTT正常发信息正常执行，第二次就不执行了，求大神解决。
