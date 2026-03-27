// Wellington Oliveira <well.oliveira.snt@gmail.com>
// https://github.com/oliveirasWell/so-2026-01-ufms

#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/list.h>
#include <linux/slab.h>

struct birthday {
    int day;
    int month;
    int year;
    struct list_head list;
};

static LIST_HEAD(birthday_list);

static const struct {
    int day, month, year;
} entries[] = {
    {  2,  8, 1995 },
    { 15,  3, 1988 },
    {  7, 11, 2001 },
    { 23,  6, 1979 },
    {  1,  1, 2000 },
};

static int __init simple_init(void)
{
    struct birthday *ptr;
    int i;

    for (i = 0; i < ARRAY_SIZE(entries); i++) {
        ptr = kmalloc(sizeof(*ptr), GFP_KERNEL);
        if (!ptr)
            return -ENOMEM;

        ptr->day   = entries[i].day;
        ptr->month = entries[i].month;
        ptr->year  = entries[i].year;
        INIT_LIST_HEAD(&ptr->list);
        list_add_tail(&ptr->list, &birthday_list);
    }

    struct list_head *pos = birthday_list.next;
    while (pos != &birthday_list) {
        ptr = list_entry(pos, struct birthday, list);
        printk(KERN_INFO "%02d/%02d/%04d\n", ptr->day, ptr->month, ptr->year);
        pos = pos->next;
    }

    return 0;
}

static void __exit simple_exit(void)
{
    struct birthday *ptr;

    while (!list_empty(&birthday_list)) {
        ptr = list_first_entry(&birthday_list, struct birthday, list);
        list_del(&ptr->list);
        kfree(ptr);
    }
}

module_init(simple_init);
module_exit(simple_exit);

MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Birthday Linked List Module");
MODULE_AUTHOR("Wellington Oliveira <well.oliveira.snt@gmail.com> | https://github.com/oliveirasWell/so-2026-01-ufms");
