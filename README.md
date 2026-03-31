# Нишевый мьюзик соса бэйби сервер (Navidrome + SoundCloud) 

Docker-контейнеры:
1. **Navidrome** - стриминговый сервер
2. **Sync-Worker** - среда с утилитами и скриптами для регулярной синхронизации библиотеки с ск

---

## Требования к хосту

* Docker и Docker Compose
* Git
* [cite_start]если сервер разворачивается на Windows, то нужно установить и подготовить WSL2 (Debian)[cite: 1].

---

## Подготовка окружения Windows (WSL2)

> Этот шаг нужен **только** если хост на Windows. При развертывании на Linux сервере можно скипнуть.

### 1. Конфигурация ресурсов и сети
[cite_start]Чтобы норм работало и не жрало ресурсы нужно задать лимиты[cite: 1].
Создай файл `.wslconfig` в (`C:\Users\USERNAME\.wslconfig`):

```ini
[wsl2]
memory=8GB
processors=6
swap=2GB
autoMemoryReclaim=dropcache
networkingMode=mirrored
localhostForwarding=true
```
[cite_start]Режим `networkingMode=mirrored` важен, если на пк поднят VPN, и необходимо пробрасывать эти настройки внутрь WSL для корректного исходящего подключения[cite: 2].

### 2. Проброс портов
[cite_start]Для доступа к серверу из локальной сети пробрось порт из Windows в WSL2[cite: 12]. Запусти PowerShell от админа и выполни:

```powershell
netsh interface portproxy add v4tov4 listenport=4533 listenaddress=0.0.0.0 connectport=4533 connectaddress=127.0.0.1
```

### 3. Настройка Брандмауэра Windows
[cite_start]Разрешаем входящие подключения для порта 4533[cite: 12]. 
[cite_start]Зайди в **Windows Defender Firewall with Advanced Security** -> **Inbound Rules** -> **Add rule**[cite: 13]. 
Параметры:
* [cite_start]**Rule type:** Port [cite: 13]
* [cite_start]**Protocol:** TCP [cite: 13]
* [cite_start]**Specific rule ports:** 4533 [cite: 13]
* [cite_start]**Action:** Allow the connection [cite: 13]
* [cite_start]**Profiles:** All (Domain, Private, Public) [cite: 13]
* [cite_start]**Name:** navidrome [cite: 13]

---

## Установка и развертывание

```bash
bash <(curl -s https://gist.githubusercontent.com/Xoxotynn/fbaa8805300f8384449b45c3dd8a5b34/raw/6c0bf162cec31d2a25357464a608037b51c45192/bootstrap.sh)
```

или

```bash
wget -qO- https://gist.githubusercontent.com/Xoxotynn/fbaa8805300f8384449b45c3dd8a5b34/raw/6c0bf162cec31d2a25357464a608037b51c45192/bootstrap.sh | bash
```


**После установки:**
```bash
cp .env.example .env
nano .env   # Заполни свои данные
./setup.sh
```

---

## Настройка доступа из интернета

[cite_start]Для доступа также нужно пробросить порт 4533 на роутере[cite: 12].

Если роутер на OpenWRT, проброс можно настроить через LuCI (раздел *Network -> Firewall -> Port Forwards*) или по SSH:

```bash
uci add firewall redirect
uci set firewall.@redirect[-1].name='Navidrome_WAN'
uci set firewall.@redirect[-1].src='wan'
uci set firewall.@redirect[-1].src_dport='4533'
uci set firewall.@redirect[-1].dest='lan'
uci set firewall.@redirect[-1].dest_ip='SERVER_LOCAL_IP'
uci set firewall.@redirect[-1].dest_port='4533'
uci set firewall.@redirect[-1].target='DNAT'
uci commit firewall
/etc/init.d/firewall restart
```

---

## Использование и управление

Интерфейс Navidrome будет доступен по адресу: `http://<ВНЕШНИЙ_IP>:4533`

Синхронизация происходит каждые 7 дней.
Если нужно **принудительно запустить синхронизацию вручную**:

```bash
docker compose exec sync-worker /app/scripts/full_sync.sh
```