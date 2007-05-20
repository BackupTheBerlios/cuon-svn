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

void
on_MiscEdit_activate                   (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_MiscSave_activate                   (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_treeMaterialgroup_row_activated     (GtkTreeView     *treeview,
                                        GtkTreePath     *path,
                                        GtkTreeViewColumn *column,
                                        gpointer         user_data);

void
on_treeArticles_row_activated          (GtkTreeView     *treeview,
                                        GtkTreePath     *path,
                                        GtkTreeViewColumn *column,
                                        gpointer         user_data);

void
on_rbQuarterly_toggled                 (GtkToggleButton *togglebutton,
                                        gpointer         user_data);

void
on_rbSemestral_toggled                 (GtkToggleButton *togglebutton,
                                        gpointer         user_data);

void
on_rbYearly_toggled                    (GtkToggleButton *togglebutton,
                                        gpointer         user_data);

void
on_lPosition_notify                    (GObject         *gobject,
                                        GParamSpec      *arg1,
                                        gpointer         user_data);

gboolean
on_Mainwindow_key_press_event          (GtkWidget       *widget,
                                        GdkEventKey     *event,
                                        gpointer         user_data);

void
on_bQuickAppend_clicked                (GtkButton       *button,
                                        gpointer         user_data);

void
on_Misc_delete1_activate               (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_accounting1_activate                (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_payment_new_activate                (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_payment_edit_activate               (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_payment_save_activate               (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_bPaymentSearchAccount_clicked       (GtkButton       *button,
                                        gpointer         user_data);

void
on_ePaymentAccountID_changed           (GtkEditable     *editable,
                                        gpointer         user_data);

void
on_list_of_invoices1_activate          (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_bSimpleCash1_clicked                (GtkButton       *button,
                                        gpointer         user_data);

void
on_bSimpleCash2_clicked                (GtkButton       *button,
                                        gpointer         user_data);

void
on_bSimpleBank1_clicked                (GtkButton       *button,
                                        gpointer         user_data);

void
on_bSimpleBank2_clicked                (GtkButton       *button,
                                        gpointer         user_data);

void
on_bSimpleBank3_clicked                (GtkButton       *button,
                                        gpointer         user_data);
