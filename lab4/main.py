from hash_table import GrammarHashTable
from models import calculate_v


def main():
    ht = GrammarHashTable(20)

    data = [
        ("Подлежащее", "Главный член предложения"),
        ("Сказуемое", "Действие предмета"),
        ("Существительное", "Часть речи, предмет"),
        ("Союз", "Служебная часть речи"),
        ("Причастие", "Признак предмета по действию"),
        ("Предлог", "Служебное слово"),
        ("Глагол", "Часть речи, действие"),
        ("Наречие", "Признак действия"),
        ("Местоимение", "Указывает на предмет"),
        ("Частица", "Вносит оттенки значения"),
    ]

    for word, desc in data:
        ht.insert(word, desc)

    while True:
        print("\nМеню:")
        print("1. Показать таблицу")
        print("2. Добавить запись")
        print("3. Удалить запись")
        print("4. Выход")
        choice = input("Выбор: ")

        if choice == "1":
            print(f"{'№':<3} | {'V':<5} | {'h(V)':<5} | {'ID':<15} | U C T D | P0 | Pi")
            print("-" * 70)
            for i, row in enumerate(ht.table):
                v = calculate_v(row.id) if row.id else 0
                h = ht.h1(v) if row.id else 0
                flags = f"{row.u} {row.c} {row.t} {row.d}"
                print(
                    f"{i:<3} | {v:<5} | {h:<5} | {row.id[:14]:<15} | {flags} | {row.p0:<2} | {row.pi[:20]}"
                )

            print(f"\nКоэффициент заполнения: {ht.get_load_factor():.2f}")

        elif choice == "2":
            ht.interactive_add()
        elif choice == "3":
            ht.interactive_delete()
        elif choice == "4":
            break


if __name__ == "__main__":
    main()
