#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/list.h>
#include <linux/slab.h>
#include <linux/types.h>

struct birthday {
    int day;
    int month;
    int year;
    struct list_head list;
};

static LIST_HEAD(birthday_list);

int simple_init(void)
{
    struct birthday *person;
    struct birthday *ptr;

    static const struct { int d, m, y; } data[5] = {
        {2,  8, 1995},
        {15, 3, 1988},
        {7,  11, 2001},
        {23, 6, 1979},
        {1,  1, 2000},
    };
    int i;

    printk(KERN_INFO "Loading Module\n");

    for (i = 0; i < 5; i++) {
        person = kmalloc(sizeof(*person), GFP_KERNEL);
        if (!person) {
            printk(KERN_ERR "kmalloc falhou no elemento %d\n", i);
            return -ENOMEM;
        }
        person->day   = data[i].d;
        person->month = data[i].m;
        person->year  = data[i].y;
        INIT_LIST_HEAD(&person->list);
        list_add_tail(&person->list, &birthday_list);
    }

    printk(KERN_INFO "--- Lista de Aniversários ---\n");
    list_for_each_entry(ptr, &birthday_list, list) {
        printk(KERN_INFO "Aniversário: %02d/%02d/%04d\n",
               ptr->day, ptr->month, ptr->year);
    }

    return 0;
}

void simple_exit(void)
{
    struct birthday *ptr, *next;

    printk(KERN_INFO "Removing Module — liberando lista\n");

    list_for_each_entry_safe(ptr, next, &birthday_list, list) {
        printk(KERN_INFO "Removendo: %02d/%02d/%04d\n",
               ptr->day, ptr->month, ptr->year);
        list_del(&ptr->list);
        kfree(ptr);
    }

    printk(KERN_INFO "Lista liberada.\n");
}

module_init(simple_init);
module_exit(simple_exit);

MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Birthday Linked List Module");
MODULE_AUTHOR("SGG");
