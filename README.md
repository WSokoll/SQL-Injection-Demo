# SQL-Injection-Demo
Aplikacja napisana przy pomocy frameworka **Flask** w celu demonstracji podatności tylu SQL injection.

## Przygotowanie środowiska
### Przykładowy sposób uruchomienia aplikacji z wykorzystaniem oprogramowania Pycharm:
1. Pierwszym krokiem jest sklonowanie repozytorium do dowolnego folderu na dysku:  
   `git clone https://github.com/WSokoll/SQL-Injection-Demo.git`
2. Następnie należy otworzyć projekt w środowisku Pycharm:
   1. Zakładka `File` -> `New Project` lub przycisk `New Project`
   2. Po lewej stronie należy wybrać z listy `Flask` (zamiast domyślnego `Pure Python`)
   3. W polu `location` należy podać ścieżkę do folderu, który został utworzony po sklonowaniu repozytorium (folder o nazwie `SQL-Injection-Demo` zawierający pliki aplikacji)
   4. Przycisk `Create` -> `Create from existing sources`
   5. Po lewej stronie, obok przycisku _run_ (zielona strzałka po prawej stronie na górnym pasku) znajduje się _Run/Debug Configuration_. Należy kliknąć w obecną konfigurację, następnie `Edit configurations`. W lewym górnym rogu przycisk `+` -> z listy wybieramy `Flask server`. Następnie przycisk `Apply` -> `OK`.
3. Ostatnim krokiem jest pobranie wymaganych bibliotek. Można to zrobić otwierając zakładkę `Terminal` (lewy dolny pasek) i wpisując komendę:
   `pip install -r .\requirements.txt`
4. Po uruchomieniu (zielona strzałka po prawej stronie na górnym pasku) aplikacja powinna być dostępna z przeglądarki pod adresem:  
   `http://127.0.0.1:5000/`

## Zadanie 1
Celem pierwszego zadania jest rekonesans. Znalezienie takiej podatności aplikacji, która umożliwi pozyskanie jak największej ilości informacji na temat struktury bazy danych.
Będziemy chcieli pozyskać takie informacje, które ułatwią rozwiązanie Zadania 2, którego celem będzie nadanie sobie samemu roli admina i tym samym uzyskanie dostępu do panelu admina.  
Aby wykonać zadanie należy:  
1. Zalogować się do aplikacji przy pomocy danych: email: `user@test.com`, hasło: `test1`
2. Znaleźć podatność aplikacji, która pozwoli na wyświetlanie dodatkowych informacji z bazy danych
3. Przy pomocy podatności i metody prób i błędów dowiedzieć się z jakiego typu bazy danych korzysta aplikacja (przykładowo zapytanie `SELECT @@version;` zadziałałoby, gdyby wykorzystano MySQL)
4. Przy pomocy podatności i odpowiedniego zapytania dowiedzieć się jak wygląda struktura tabel w bazie (nazwy tabel, pola i typy pól w tabelach). Przede wszystkim interesować nas będą tabele związane z użytkownikami i rolami
5. Przy pomocy podatności dowiedzieć się jakie id należy przypisać użytkownikowi (oraz w jaki sposób należy je przypisać), aby uzyskał on rolę admina

Podpowiedź: Jeżeli potrzebujemy uzyskać z danej tabeli dwie kolumny, ale "mamy do dyspozycji" tylko jedną, przydatne może być łączenie zawartości dwóch kolumn w jedną. Przykładowo `SELECT name||'~'||surname FROM example_table;` zwróci jedną kolumnę.

## Zadanie 2
Celem tego zadania jest podmiana danych w bazie w taki sposób, aby użytkownik `user@test.com` uzyskał dostęp do panelu administratora.
Należy wykorzystać wiedzę zdobytą w Zadaniu 1. Podatność, która umożliwi taką operację, znajduje się na podstronie account.

Podpowiedź: Sprawdź jak wygląda adres url podstrony account, z czego się składa i czy można go w pewien sposób zmodyfikować (500ka rzucana przez aplikację niekoniecznie musi być złym znakiem ;).

## Zadanie 3
Wymień i opisz przynajmniej dwa sposoby na zabezpieczenie się przed atakami przeprowadzonymi w zadaniu 1 oraz 2.
