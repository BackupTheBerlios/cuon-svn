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

void
on_gdeDate_date_changed                (GnomeDateEdit   *gnomedateedit,
                                        gpointer         user_data);

void
on_gdeDate_time_changed                (GnomeDateEdit   *gnomedateedit,
                                        gpointer         user_data);

void
on_bShowDMS_clicked                    (GtkButton       *button,
                                        gpointer         user_data);

void
on_bShowPartnerDMS_clicked             (GtkButton       *button,
                                        gpointer         user_data);

void
on_eDate_changed                       (GtkEditable     *editable,
                                        gpointer         user_data);

void
on_calendar1_day_selected_double_click (GtkCalendar     *calendar,
                                        gpointer         user_data);

void
on_calendar1_state_changed             (GtkWidget       *widget,
                                        GtkStateType     state,
                                        gpointer         user_data);

void
on_eSchedulDate_changed                (GtkEditable     *editable,
                                        gpointer         user_data);

void
on_eSchedulCallerID_changed            (GtkEditable     *editable,
                                        gpointer         user_data);

void
on_bChooseCaller_clicked               (GtkButton       *button,
                                        gpointer         user_data);

void
on_eSchedulRepID_changed               (GtkEditable     *editable,
                                        gpointer         user_data);

void
on_bChooseRep_clicked                  (GtkButton       *button,
                                        gpointer         user_data);

void
on_eSchedulContractID_changed          (GtkEditable     *editable,
                                        gpointer         user_data);

void
on_bank_new1_activate                  (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_bank_save1_activate                 (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_bank_edit1_activate                 (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

gboolean
on_key_press_event                     (GtkWidget       *widget,
                                        GdkEventKey     *event,
                                        gpointer         user_data);

void
on_bChooseBank_clicked                 (GtkButton       *button,
                                        gpointer         user_data);

void
on_eBankID_changed                     (GtkEditable     *editable,
                                        gpointer         user_data);

void
on_bSchedulLetter_clicked              (GtkButton       *button,
                                        gpointer         user_data);

void
on_bSchedulEmail_clicked               (GtkButton       *button,
                                        gpointer         user_data);

void
on_bSchedulDMS_clicked                 (GtkButton       *button,
                                        gpointer         user_data);

gboolean
on_eSearch_key_press_event             (GtkWidget       *widget,
                                        GdkEventKey     *event,
                                        gpointer         user_data);

gboolean
on_key_press_event                     (GtkWidget       *widget,
                                        GdkEventKey     *event,
                                        gpointer         user_data);

gboolean
on_press_event                         (GtkWidget       *widget,
                                        GdkEventKey     *event,
                                        gpointer         user_data);

void
on_bLetter_clicked                     (GtkButton       *button,
                                        gpointer         user_data);

void
on_bPartnerLetter_clicked              (GtkButton       *button,
                                        gpointer         user_data);

void
on_bSchedulLetter_clicked              (GtkButton       *button,
                                        gpointer         user_data);

gboolean
on_eSearch_key_press_event             (GtkWidget       *widget,
                                        GdkEventKey     *event,
                                        gpointer         user_data);

gboolean
on_eSearch_key_press_event             (GtkWidget       *widget,
                                        GdkEventKey     *event,
                                        gpointer         user_data);

void
on_eAddressCallerID_changed            (GtkEditable     *editable,
                                        gpointer         user_data);

void
on_bChooseCaller_clicked               (GtkButton       *button,
                                        gpointer         user_data);

void
on_bChooseContract_clicked             (GtkButton       *button,
                                        gpointer         user_data);

gboolean
on_comboboxentry_entry1_key_press_event
                                        (GtkWidget       *widget,
                                        GdkEventKey     *event,
                                        gpointer         user_data);

gboolean
on_comboboxentry_entry2_key_press_event
                                        (GtkWidget       *widget,
                                        GdkEventKey     *event,
                                        gpointer         user_data);

void
on_bContact_clicked                    (GtkButton       *button,
                                        gpointer         user_data);

void
on_edit1_activate                      (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_calendar1_day_selected_double_click (GtkCalendar     *calendar,
                                        gpointer         user_data);

void
on_eDate_changed                       (GtkEditable     *editable,
                                        gpointer         user_data);

void
on_new1_activate                       (GtkToolButton   *toolbutton,
                                        gpointer         user_data);

void
on_edit1_activate                      (GtkToolButton   *toolbutton,
                                        gpointer         user_data);

void
on_save1_activate                      (GtkToolButton   *toolbutton,
                                        gpointer         user_data);

void
on_edit1_activate                      (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_new1_activate                       (GtkToolButton   *toolbutton,
                                        gpointer         user_data);

void
on_save1_activate                      (GtkToolButton   *toolbutton,
                                        gpointer         user_data);

void
on_calendar1_day_selected_double_click (GtkCalendar     *calendar,
                                        gpointer         user_data);

void
on_eDate_changed                       (GtkEditable     *editable,
                                        gpointer         user_data);

void
on_edit1_activate                      (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_new1_activate                       (GtkToolButton   *toolbutton,
                                        gpointer         user_data);

void
on_save1_activate                      (GtkToolButton   *toolbutton,
                                        gpointer         user_data);

void
on_calendar1_day_selected_double_click (GtkCalendar     *calendar,
                                        gpointer         user_data);

void
on_eDate_changed                       (GtkEditable     *editable,
                                        gpointer         user_data);

void
on_rbDay_clicked                       (GtkButton       *button,
                                        gpointer         user_data);

void
on_rbHour_clicked                      (GtkButton       *button,
                                        gpointer         user_data);

void
on_rbMinute_clicked                    (GtkButton       *button,
                                        gpointer         user_data);

void
on_bGoToAddress_clicked                (GtkButton       *button,
                                        gpointer         user_data);

void
on_bAddFormular2NoticesMisc_clicked    (GtkButton       *button,
                                        gpointer         user_data);

void
on_bAddFormulat2NoticesContacter_clicked
                                        (GtkButton       *button,
                                        gpointer         user_data);

void
on_bAddformular2NoticesRep_clicked     (GtkButton       *button,
                                        gpointer         user_data);

void
on_bAddFormular2NotesSalesman_clicked  (GtkButton       *button,
                                        gpointer         user_data);

void
on_bChooseSalesman_clicked             (GtkButton       *button,
                                        gpointer         user_data);

void
on_notes1_activate                     (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_NotesNew_activate                   (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_NotesEdit1_activate                 (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_NotesSave_activate                  (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_bAddNameMisc_clicked                (GtkButton       *button,
                                        gpointer         user_data);

void
on_bAddNameContacter_clicked           (GtkButton       *button,
                                        gpointer         user_data);

void
on_bAddNameRep_clicked                 (GtkButton       *button,
                                        gpointer         user_data);

void
on_bAddnameSalesman_clicked            (GtkButton       *button,
                                        gpointer         user_data);

void
on_bSendEmailAddress_clicked           (GtkButton       *button,
                                        gpointer         user_data);

void
on_bSendEmailPartner_clicked           (GtkButton       *button,
                                        gpointer         user_data);

void
on_bSendEmailSchedul_clicked           (GtkButton       *button,
                                        gpointer         user_data);

void
on_bGeneratePartner_clicked            (GtkButton       *button,
                                        gpointer         user_data);

void
on_bAddFormular2NotesMisc_clicked      (GtkButton       *button,
                                        gpointer         user_data);

void
on_bAddFormular2NotesContacter_clicked (GtkButton       *button,
                                        gpointer         user_data);

void
on_bAddformular2NotesRep_clicked       (GtkButton       *button,
                                        gpointer         user_data);

void
on_calSchedulStaff_day_selected        (GtkCalendar     *calendar,
                                        gpointer         user_data);

void
on_calSchedulStaff_day_selected_double_click
                                        (GtkCalendar     *calendar,
                                        gpointer         user_data);

void
on_treeScheduls_row_activated          (GtkTreeView     *treeview,
                                        GtkTreePath     *path,
                                        GtkTreeViewColumn *column,
                                        gpointer         user_data);

void
on_bGotoSchedulAddress_clicked         (GtkButton       *button,
                                        gpointer         user_data);

void
on_set_ready1_activate                 (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_set_ready1_activate                 (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_bQuit_clicked                       (GtkButton       *button,
                                        gpointer         user_data);

void
on_bViewHomepage_clicked               (GtkButton       *button,
                                        gpointer         user_data);

void
on_bSendMail_clicked                   (GtkButton       *button,
                                        gpointer         user_data);

void
on_bSendPartnerEmail_clicked           (GtkButton       *button,
                                        gpointer         user_data);

void
on_bPartnerViewHomepage_clicked        (GtkButton       *button,
                                        gpointer         user_data);

void
on_newsletter1_activate                (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_newsletter_email_activate           (GtkMenuItem     *menuitem,
                                        gpointer         user_data);

void
on_newsletter_print_activate           (GtkMenuItem     *menuitem,
                                        gpointer         user_data);
