#include <gnome.h>


void
on_print_setup1_activate               (GtkMenuItem     *menuitem,
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
on_delete1_activate                    (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_PositionNew1_activate               (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on__PositionEdit1_activate             (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_PositionSave1_activate              (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_PositionPrint1_activate             (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_PositionClear1_activate             (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_bSearch_clicked                     (GtkButton       *button,
                                        gpointer         user_data);

void
on_eAddressNumber_changed              (GtkEditable     *editable,
                                        gpointer         user_data);

void
on_bSearchCustom_clicked               (GtkButton       *button,
                                        gpointer         user_data);

void
on_bSearchSupply_clicked               (GtkButton       *button,
                                        gpointer         user_data);

void
on_bSearchGet_clicked                  (GtkButton       *button,
                                        gpointer         user_data);

void
on_SupplyNew1_activate                 (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_SupplyEdit1_activate                (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_SupplySave1_activate                (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_SupplyClear1_activate               (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_GetsNew1_activate                   (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_GetsEdit1_activate                  (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_GetsSave1_activate                  (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_GetsClear1_activate                 (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_notebook1_switch_page               (GtkNotebook     *notebook,
                                        GtkNotebookPage *page,
                                        guint            page_num,
                                        gpointer         user_data);

void
on_bArticleSearch_clicked              (GtkButton       *button,
                                        gpointer         user_data);

void
on_print_invoice1_activate             (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_print_delivery_note1_activate       (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_print_pickup_note1_activate         (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_PositionEdit1_activate              (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_eSupplyNumber_changed               (GtkEditable     *editable,
                                        gpointer         user_data);

void
on_eGetsNumber_changed                 (GtkEditable     *editable,
                                        gpointer         user_data);

void
on_bSearchForwardingAgency_clicked     (GtkButton       *button,
                                        gpointer         user_data);

void
on_bContactPerson_clicked              (GtkButton       *button,
                                        gpointer         user_data);

void
on_eArticleID_changed                  (GtkEditable     *editable,
                                        gpointer         user_data);
