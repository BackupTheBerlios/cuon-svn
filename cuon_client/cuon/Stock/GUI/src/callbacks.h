#include <gnome.h>


void
on_print_setup1_activate               (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_New1_activate                       (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_Edit1_activate                      (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_Save1_activate                      (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_Delete1_activate                    (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_GoodsNew1_activate                  (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_GoogsEdit1_activate                 (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_GoodsSave1_activate                 (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_GoodsClear1_activate                (GtkMenuItem     *menuitem,
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
on_quit1_activate                      (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_GoodsEdit1_activate                 (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_bArticleSearch_clicked              (GtkButton       *button,
                                        gpointer         user_data);

void
on_eArticleID_changed                  (GtkEditable     *editable,
                                        gpointer         user_data);
