#include <gnome.h>


void
on_choosePrinter1_activate             (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_quit1_activate                      (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_new1_activate                       (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_edit1_activate                      (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_save1_activate                      (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_print1_activate                     (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_clear1_activate                     (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_bSearch_clicked                     (GtkButton       *button,
                                        gpointer         user_data);

void
on_notebook1_switch_page               (GtkNotebook     *notebook,
                                        GtkNotebookPage *page,
                                        guint            page_num,
                                        gpointer         user_data);

void
on_VatNew1_activate                    (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_VatEdit1_activate                   (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_vatsave1_activate                   (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_vatprint1_activate                  (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_vatclear1_activate                  (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_VatSave1_activate                   (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_VatPrint1_activate                  (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_VatClear1_activate                  (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_bImportAcct_clicked                 (GtkButton       *button,
                                        gpointer         user_data);
