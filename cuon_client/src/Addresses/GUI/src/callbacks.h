#include <gtk/gtk.h>


void
on_choosePrinter1_activate             (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_quit1_activate                      (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_undo1_activate                      (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_find1_activate                      (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_new1_activate                       (GtkMenuItem     *menuitem,
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
on_bank1_activate                      (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_newBank_activate                    (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_misc1_activate                      (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_PartnerNew1_activate                (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_PartnerSave1_activate               (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_mi_PartnerPrint1_activate           (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_PartnerDelete1_activate             (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_schedul1_activate                   (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_SchedulNew_activate                 (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_SchedulSave_activate                (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_liAddressesPhone1_activate          (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_newletter1_activate                 (GtkMenuItem     *menuitem,
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
on_MiscSave1_activate                  (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_chooseAddress_activate              (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_edit1_activate                      (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_BankNew1_activate                   (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_BankEdit1_activate                  (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_MiscEdit1_activate                  (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_PartnerEdit1_activate               (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_SchedulEdit1_activate               (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_liAddressesPhone11_activate         (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_eSchedulDate_changed                (GtkEditable     *editable,
                                        gpointer         user_data);

void
on_calendar1_day_selected              (GtkCalendar     *calendar,
                                        gpointer         user_data);

void
on_hscale1_value_changed               (GtkRange        *range,
                                        gpointer         user_data);

void
on_vscale1_value_changed               (GtkRange        *range,
                                        gpointer         user_data);
