/*
 * DO NOT EDIT THIS FILE - it is generated by Glade.
 */

#ifdef HAVE_CONFIG_H
#  include <config.h>
#endif

#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>

#include <gdk/gdkkeysyms.h>
#include <gtk/gtk.h>

#include "callbacks.h"
#include "interface.h"
#include "support.h"

#define GLADE_HOOKUP_OBJECT(component,widget,name) \
  g_object_set_data_full (G_OBJECT (component), name, \
    gtk_widget_ref (widget), (GDestroyNotify) gtk_widget_unref)

#define GLADE_HOOKUP_OBJECT_NO_REF(component,widget,name) \
  g_object_set_data (G_OBJECT (component), name, widget)

GtkWidget*
create_window1 (void)
{
  GtkWidget *window1;
  GdkPixbuf *window1_icon_pixbuf;
  GtkWidget *vbox1;
  GtkWidget *menubar1;
  GtkWidget *connect1;
  GtkWidget *connect1_menu;
  GtkWidget *login1;
  GtkWidget *logout1;
  GtkWidget *trennlinie1;
  GtkWidget *end1;
  GtkWidget *image8;
  GtkWidget *data;
  GtkWidget *data_menu;
  GtkWidget *mi_addresses1;
  GtkWidget *mi_articles1;
  GtkWidget *bank1;
  GtkWidget *trennlinie3;
  GtkWidget *mi_bibliographic;
  GtkWidget *mi_staff1;
  GtkWidget *trennlinie4;
  GtkWidget *contracts1;
  GtkWidget *contracts1_menu;
  GtkWidget *mi_insurances1;
  GtkWidget *mi_rent1;
  GtkWidget *mi_leasing1;
  GtkWidget *separator3;
  GtkWidget *mi_clients1;
  GtkWidget *action1;
  GtkWidget *action1_menu;
  GtkWidget *mi_order1;
  GtkWidget *mi_stock1;
  GtkWidget *mi_dms1;
  GtkWidget *accounting1;
  GtkWidget *accounting1_menu;
  GtkWidget *mi_cash_account_book1;
  GtkWidget *extras;
  GtkWidget *extras_menu;
  GtkWidget *mayavi1;
  GtkWidget *mayavi1_menu;
  GtkWidget *mi_test1;
  GtkWidget *mi_expert_system1;
  GtkWidget *mi_project1;
  GtkWidget *trennlinie5;
  GtkWidget *tools;
  GtkWidget *tools_menu;
  GtkWidget *preferences1;
  GtkWidget *preferences1_menu;
  GtkWidget *mi_user1;
  GtkWidget *mi_finances1;
  GtkWidget *update1;
  GtkWidget *mi_report_generator1;
  GtkWidget *mi_webshop1;
  GtkWidget *separator1;
  GtkWidget *databases1;
  GtkWidget *trennlinie2;
  GtkWidget *mi_import_data1;
  GtkWidget *help1;
  GtkWidget *help1_menu;
  GtkWidget *about1;
  GtkWidget *onlinehelp;
  GtkWidget *table1;
  GtkWidget *label1;
  GtkWidget *eUserName;
  GtkWidget *label2;
  GtkWidget *eServer;
  GtkWidget *label3;
  GtkWidget *eAppServer;
  GtkWidget *label4;
  GtkWidget *eDatabase;
  GtkWidget *label5;
  GtkWidget *eWebshop;
  GtkWidget *hbox1;
  GtkWidget *scrolledwindow3;
  GtkWidget *tree1;
  GtkWidget *vbox3;
  GtkWidget *scrolledwindow4;
  GtkWidget *tvEvents;
  GtkWidget *calendar1;
  GtkTooltips *tooltips;

  tooltips = gtk_tooltips_new ();

  window1 = gtk_window_new (GTK_WINDOW_TOPLEVEL);
  gtk_widget_set_size_request (window1, 1024, 720);
  gtk_window_set_title (GTK_WINDOW (window1), _("Client PyCuon"));
  gtk_window_set_default_size (GTK_WINDOW (window1), 662, 142);
  gtk_window_set_resizable (GTK_WINDOW (window1), FALSE);
  window1_icon_pixbuf = create_pixbuf ("cuon-logo.xpm");
  if (window1_icon_pixbuf)
    {
      gtk_window_set_icon (GTK_WINDOW (window1), window1_icon_pixbuf);
      gdk_pixbuf_unref (window1_icon_pixbuf);
    }

  vbox1 = gtk_vbox_new (FALSE, 0);
  gtk_widget_show (vbox1);
  gtk_container_add (GTK_CONTAINER (window1), vbox1);

  menubar1 = gtk_menu_bar_new ();
  gtk_widget_show (menubar1);
  gtk_box_pack_start (GTK_BOX (vbox1), menubar1, FALSE, FALSE, 0);

  connect1 = gtk_menu_item_new_with_mnemonic (_("Connect"));
  gtk_widget_show (connect1);
  gtk_container_add (GTK_CONTAINER (menubar1), connect1);

  connect1_menu = gtk_menu_new ();
  gtk_menu_item_set_submenu (GTK_MENU_ITEM (connect1), connect1_menu);

  login1 = gtk_menu_item_new_with_mnemonic (_("Login"));
  gtk_widget_show (login1);
  gtk_container_add (GTK_CONTAINER (connect1_menu), login1);

  logout1 = gtk_menu_item_new_with_mnemonic (_("Logout"));
  gtk_widget_show (logout1);
  gtk_container_add (GTK_CONTAINER (connect1_menu), logout1);

  trennlinie1 = gtk_separator_menu_item_new ();
  gtk_widget_show (trennlinie1);
  gtk_container_add (GTK_CONTAINER (connect1_menu), trennlinie1);
  gtk_widget_set_sensitive (trennlinie1, FALSE);

  end1 = gtk_image_menu_item_new_with_mnemonic (_("quit"));
  gtk_widget_show (end1);
  gtk_container_add (GTK_CONTAINER (connect1_menu), end1);
  gtk_tooltips_set_tip (tooltips, end1, _("Close the Application"), NULL);

  image8 = gtk_image_new_from_stock ("gtk-quit", GTK_ICON_SIZE_MENU);
  gtk_widget_show (image8);
  gtk_image_menu_item_set_image (GTK_IMAGE_MENU_ITEM (end1), image8);

  data = gtk_menu_item_new_with_mnemonic (_("Data"));
  gtk_widget_show (data);
  gtk_container_add (GTK_CONTAINER (menubar1), data);

  data_menu = gtk_menu_new ();
  gtk_menu_item_set_submenu (GTK_MENU_ITEM (data), data_menu);

  mi_addresses1 = gtk_menu_item_new_with_mnemonic (_("_Addresses"));
  gtk_widget_show (mi_addresses1);
  gtk_container_add (GTK_CONTAINER (data_menu), mi_addresses1);

  mi_articles1 = gtk_menu_item_new_with_mnemonic (_("Arti_cles"));
  gtk_widget_show (mi_articles1);
  gtk_container_add (GTK_CONTAINER (data_menu), mi_articles1);

  bank1 = gtk_menu_item_new_with_mnemonic (_("Bank"));
  gtk_widget_show (bank1);
  gtk_container_add (GTK_CONTAINER (data_menu), bank1);

  trennlinie3 = gtk_separator_menu_item_new ();
  gtk_widget_show (trennlinie3);
  gtk_container_add (GTK_CONTAINER (data_menu), trennlinie3);
  gtk_widget_set_sensitive (trennlinie3, FALSE);

  mi_bibliographic = gtk_menu_item_new_with_mnemonic (_("Bibliographic"));
  gtk_widget_show (mi_bibliographic);
  gtk_container_add (GTK_CONTAINER (data_menu), mi_bibliographic);

  mi_staff1 = gtk_menu_item_new_with_mnemonic (_("Staff"));
  gtk_widget_show (mi_staff1);
  gtk_container_add (GTK_CONTAINER (data_menu), mi_staff1);

  trennlinie4 = gtk_separator_menu_item_new ();
  gtk_widget_show (trennlinie4);
  gtk_container_add (GTK_CONTAINER (data_menu), trennlinie4);
  gtk_widget_set_sensitive (trennlinie4, FALSE);

  contracts1 = gtk_menu_item_new_with_mnemonic (_("Contracts"));
  gtk_widget_show (contracts1);
  gtk_container_add (GTK_CONTAINER (data_menu), contracts1);

  contracts1_menu = gtk_menu_new ();
  gtk_menu_item_set_submenu (GTK_MENU_ITEM (contracts1), contracts1_menu);

  mi_insurances1 = gtk_menu_item_new_with_mnemonic (_("Insurances"));
  gtk_widget_show (mi_insurances1);
  gtk_container_add (GTK_CONTAINER (contracts1_menu), mi_insurances1);

  mi_rent1 = gtk_menu_item_new_with_mnemonic (_("Rent"));
  gtk_widget_show (mi_rent1);
  gtk_container_add (GTK_CONTAINER (contracts1_menu), mi_rent1);

  mi_leasing1 = gtk_menu_item_new_with_mnemonic (_("Leasing"));
  gtk_widget_show (mi_leasing1);
  gtk_container_add (GTK_CONTAINER (contracts1_menu), mi_leasing1);

  separator3 = gtk_separator_menu_item_new ();
  gtk_widget_show (separator3);
  gtk_container_add (GTK_CONTAINER (data_menu), separator3);
  gtk_widget_set_sensitive (separator3, FALSE);

  mi_clients1 = gtk_menu_item_new_with_mnemonic (_("Clients"));
  gtk_widget_show (mi_clients1);
  gtk_container_add (GTK_CONTAINER (data_menu), mi_clients1);

  action1 = gtk_menu_item_new_with_mnemonic (_("Action"));
  gtk_widget_show (action1);
  gtk_container_add (GTK_CONTAINER (menubar1), action1);

  action1_menu = gtk_menu_new ();
  gtk_menu_item_set_submenu (GTK_MENU_ITEM (action1), action1_menu);

  mi_order1 = gtk_menu_item_new_with_mnemonic (_("_Order"));
  gtk_widget_show (mi_order1);
  gtk_container_add (GTK_CONTAINER (action1_menu), mi_order1);

  mi_stock1 = gtk_menu_item_new_with_mnemonic (_("Stock"));
  gtk_widget_show (mi_stock1);
  gtk_container_add (GTK_CONTAINER (action1_menu), mi_stock1);

  mi_dms1 = gtk_menu_item_new_with_mnemonic (_("DMS"));
  gtk_widget_show (mi_dms1);
  gtk_container_add (GTK_CONTAINER (action1_menu), mi_dms1);

  accounting1 = gtk_menu_item_new_with_mnemonic (_("Accounting"));
  gtk_widget_show (accounting1);
  gtk_container_add (GTK_CONTAINER (menubar1), accounting1);

  accounting1_menu = gtk_menu_new ();
  gtk_menu_item_set_submenu (GTK_MENU_ITEM (accounting1), accounting1_menu);

  mi_cash_account_book1 = gtk_menu_item_new_with_mnemonic (_("cash account book"));
  gtk_widget_show (mi_cash_account_book1);
  gtk_container_add (GTK_CONTAINER (accounting1_menu), mi_cash_account_book1);

  extras = gtk_menu_item_new_with_mnemonic (_("Extras"));
  gtk_widget_show (extras);
  gtk_container_add (GTK_CONTAINER (menubar1), extras);

  extras_menu = gtk_menu_new ();
  gtk_menu_item_set_submenu (GTK_MENU_ITEM (extras), extras_menu);

  mayavi1 = gtk_menu_item_new_with_mnemonic (_("Mayavi"));
  gtk_widget_show (mayavi1);
  gtk_container_add (GTK_CONTAINER (extras_menu), mayavi1);

  mayavi1_menu = gtk_menu_new ();
  gtk_menu_item_set_submenu (GTK_MENU_ITEM (mayavi1), mayavi1_menu);

  mi_test1 = gtk_menu_item_new_with_mnemonic (_("Test"));
  gtk_widget_show (mi_test1);
  gtk_container_add (GTK_CONTAINER (mayavi1_menu), mi_test1);

  mi_expert_system1 = gtk_menu_item_new_with_mnemonic (_("Expert System"));
  gtk_widget_show (mi_expert_system1);
  gtk_container_add (GTK_CONTAINER (extras_menu), mi_expert_system1);

  mi_project1 = gtk_menu_item_new_with_mnemonic (_("Project"));
  gtk_widget_show (mi_project1);
  gtk_container_add (GTK_CONTAINER (extras_menu), mi_project1);

  trennlinie5 = gtk_separator_menu_item_new ();
  gtk_widget_show (trennlinie5);
  gtk_container_add (GTK_CONTAINER (extras_menu), trennlinie5);
  gtk_widget_set_sensitive (trennlinie5, FALSE);

  tools = gtk_menu_item_new_with_mnemonic (_("Tools"));
  gtk_widget_show (tools);
  gtk_container_add (GTK_CONTAINER (menubar1), tools);

  tools_menu = gtk_menu_new ();
  gtk_menu_item_set_submenu (GTK_MENU_ITEM (tools), tools_menu);

  preferences1 = gtk_menu_item_new_with_mnemonic (_("Preferences"));
  gtk_widget_show (preferences1);
  gtk_container_add (GTK_CONTAINER (tools_menu), preferences1);

  preferences1_menu = gtk_menu_new ();
  gtk_menu_item_set_submenu (GTK_MENU_ITEM (preferences1), preferences1_menu);

  mi_user1 = gtk_menu_item_new_with_mnemonic (_("User"));
  gtk_widget_show (mi_user1);
  gtk_container_add (GTK_CONTAINER (preferences1_menu), mi_user1);

  mi_finances1 = gtk_menu_item_new_with_mnemonic (_("Finances"));
  gtk_widget_show (mi_finances1);
  gtk_container_add (GTK_CONTAINER (preferences1_menu), mi_finances1);

  update1 = gtk_menu_item_new_with_mnemonic (_("Update"));
  gtk_widget_show (update1);
  gtk_container_add (GTK_CONTAINER (tools_menu), update1);

  mi_report_generator1 = gtk_menu_item_new_with_mnemonic (_("Report-Generator"));
  gtk_widget_show (mi_report_generator1);
  gtk_container_add (GTK_CONTAINER (tools_menu), mi_report_generator1);

  mi_webshop1 = gtk_menu_item_new_with_mnemonic (_("WebShop"));
  gtk_widget_show (mi_webshop1);
  gtk_container_add (GTK_CONTAINER (tools_menu), mi_webshop1);

  separator1 = gtk_separator_menu_item_new ();
  gtk_widget_show (separator1);
  gtk_container_add (GTK_CONTAINER (tools_menu), separator1);
  gtk_widget_set_sensitive (separator1, FALSE);

  databases1 = gtk_menu_item_new_with_mnemonic (_("Databases"));
  gtk_widget_show (databases1);
  gtk_container_add (GTK_CONTAINER (tools_menu), databases1);

  trennlinie2 = gtk_separator_menu_item_new ();
  gtk_widget_show (trennlinie2);
  gtk_container_add (GTK_CONTAINER (tools_menu), trennlinie2);
  gtk_widget_set_sensitive (trennlinie2, FALSE);

  mi_import_data1 = gtk_menu_item_new_with_mnemonic (_("Import Data"));
  gtk_widget_show (mi_import_data1);
  gtk_container_add (GTK_CONTAINER (tools_menu), mi_import_data1);

  help1 = gtk_menu_item_new_with_mnemonic (_("Help"));
  gtk_widget_show (help1);
  gtk_container_add (GTK_CONTAINER (menubar1), help1);

  help1_menu = gtk_menu_new ();
  gtk_menu_item_set_submenu (GTK_MENU_ITEM (help1), help1_menu);

  about1 = gtk_menu_item_new_with_mnemonic (_("About"));
  gtk_widget_show (about1);
  gtk_container_add (GTK_CONTAINER (help1_menu), about1);

  onlinehelp = gtk_menu_item_new_with_mnemonic (_("Online-Help"));
  gtk_widget_show (onlinehelp);
  gtk_container_add (GTK_CONTAINER (help1_menu), onlinehelp);

  table1 = gtk_table_new (3, 4, FALSE);
  gtk_widget_show (table1);
  gtk_box_pack_start (GTK_BOX (vbox1), table1, FALSE, FALSE, 0);

  label1 = gtk_label_new (_("connected user"));
  gtk_widget_show (label1);
  gtk_table_attach (GTK_TABLE (table1), label1, 0, 1, 0, 1,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_misc_set_alignment (GTK_MISC (label1), 0, 0.5);

  eUserName = gtk_entry_new ();
  gtk_widget_show (eUserName);
  gtk_table_attach (GTK_TABLE (table1), eUserName, 1, 2, 0, 1,
                    (GtkAttachOptions) (GTK_EXPAND | GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_widget_set_sensitive (eUserName, FALSE);
  GTK_WIDGET_UNSET_FLAGS (eUserName, GTK_CAN_FOCUS);
  gtk_editable_set_editable (GTK_EDITABLE (eUserName), FALSE);

  label2 = gtk_label_new (_("connected server"));
  gtk_widget_show (label2);
  gtk_table_attach (GTK_TABLE (table1), label2, 0, 1, 1, 2,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_misc_set_alignment (GTK_MISC (label2), 0, 0.5);

  eServer = gtk_entry_new ();
  gtk_widget_show (eServer);
  gtk_table_attach (GTK_TABLE (table1), eServer, 1, 2, 1, 2,
                    (GtkAttachOptions) (GTK_EXPAND | GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_widget_set_sensitive (eServer, FALSE);
  GTK_WIDGET_UNSET_FLAGS (eServer, GTK_CAN_FOCUS);
  gtk_editable_set_editable (GTK_EDITABLE (eServer), FALSE);

  label3 = gtk_label_new (_("Application-Server"));
  gtk_widget_show (label3);
  gtk_table_attach (GTK_TABLE (table1), label3, 2, 3, 0, 1,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_misc_set_alignment (GTK_MISC (label3), 0, 0.5);

  eAppServer = gtk_entry_new ();
  gtk_widget_show (eAppServer);
  gtk_table_attach (GTK_TABLE (table1), eAppServer, 3, 4, 0, 1,
                    (GtkAttachOptions) (GTK_EXPAND | GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_editable_set_editable (GTK_EDITABLE (eAppServer), FALSE);

  label4 = gtk_label_new (_("Database"));
  gtk_widget_show (label4);
  gtk_table_attach (GTK_TABLE (table1), label4, 2, 3, 1, 2,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_misc_set_alignment (GTK_MISC (label4), 0, 0.5);

  eDatabase = gtk_entry_new ();
  gtk_widget_show (eDatabase);
  gtk_table_attach (GTK_TABLE (table1), eDatabase, 3, 4, 1, 2,
                    (GtkAttachOptions) (GTK_EXPAND | GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_editable_set_editable (GTK_EDITABLE (eDatabase), FALSE);

  label5 = gtk_label_new (_("Web-Shop"));
  gtk_widget_show (label5);
  gtk_table_attach (GTK_TABLE (table1), label5, 2, 3, 2, 3,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_misc_set_alignment (GTK_MISC (label5), 0, 0.5);

  eWebshop = gtk_entry_new ();
  gtk_widget_show (eWebshop);
  gtk_table_attach (GTK_TABLE (table1), eWebshop, 3, 4, 2, 3,
                    (GtkAttachOptions) (GTK_EXPAND | GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_editable_set_editable (GTK_EDITABLE (eWebshop), FALSE);

  hbox1 = gtk_hbox_new (FALSE, 0);
  gtk_widget_show (hbox1);
  gtk_box_pack_start (GTK_BOX (vbox1), hbox1, TRUE, TRUE, 0);

  scrolledwindow3 = gtk_scrolled_window_new (NULL, NULL);
  gtk_widget_show (scrolledwindow3);
  gtk_box_pack_start (GTK_BOX (hbox1), scrolledwindow3, TRUE, TRUE, 0);
  gtk_scrolled_window_set_shadow_type (GTK_SCROLLED_WINDOW (scrolledwindow3), GTK_SHADOW_IN);

  tree1 = gtk_tree_view_new ();
  gtk_widget_show (tree1);
  gtk_container_add (GTK_CONTAINER (scrolledwindow3), tree1);

  vbox3 = gtk_vbox_new (FALSE, 0);
  gtk_widget_show (vbox3);
  gtk_box_pack_start (GTK_BOX (hbox1), vbox3, TRUE, TRUE, 0);

  scrolledwindow4 = gtk_scrolled_window_new (NULL, NULL);
  gtk_widget_show (scrolledwindow4);
  gtk_box_pack_start (GTK_BOX (vbox3), scrolledwindow4, TRUE, TRUE, 0);
  gtk_scrolled_window_set_shadow_type (GTK_SCROLLED_WINDOW (scrolledwindow4), GTK_SHADOW_IN);

  tvEvents = gtk_text_view_new ();
  gtk_widget_show (tvEvents);
  gtk_container_add (GTK_CONTAINER (scrolledwindow4), tvEvents);

  calendar1 = gtk_calendar_new ();
  gtk_widget_show (calendar1);
  gtk_box_pack_start (GTK_BOX (vbox3), calendar1, TRUE, TRUE, 0);
  gtk_calendar_display_options (GTK_CALENDAR (calendar1),
                                GTK_CALENDAR_SHOW_HEADING
                                | GTK_CALENDAR_SHOW_DAY_NAMES);

  g_signal_connect ((gpointer) login1, "activate_item",
                    G_CALLBACK (on_login1_activate),
                    NULL);
  g_signal_connect ((gpointer) login1, "activate",
                    G_CALLBACK (on_login1_activate),
                    NULL);
  g_signal_connect ((gpointer) logout1, "activate",
                    G_CALLBACK (on_logout1_activate),
                    NULL);
  g_signal_connect ((gpointer) end1, "activate",
                    G_CALLBACK (on_end1_activate),
                    NULL);
  g_signal_connect ((gpointer) mi_addresses1, "activate",
                    G_CALLBACK (on_addresses1_activate),
                    NULL);
  g_signal_connect ((gpointer) mi_articles1, "activate",
                    G_CALLBACK (on_articles1_activate),
                    NULL);
  g_signal_connect ((gpointer) bank1, "activate",
                    G_CALLBACK (on_bank1_activate),
                    NULL);
  g_signal_connect ((gpointer) mi_bibliographic, "activate",
                    G_CALLBACK (on_bibliographic_activate),
                    NULL);
  g_signal_connect ((gpointer) mi_staff1, "activate",
                    G_CALLBACK (on_staff1_activate),
                    NULL);
  g_signal_connect ((gpointer) mi_insurances1, "activate",
                    G_CALLBACK (on_insurances1_activate),
                    NULL);
  g_signal_connect ((gpointer) mi_rent1, "activate",
                    G_CALLBACK (on_rent1_activate),
                    NULL);
  g_signal_connect ((gpointer) mi_leasing1, "activate",
                    G_CALLBACK (on_leasing1_activate),
                    NULL);
  g_signal_connect ((gpointer) mi_clients1, "activate",
                    G_CALLBACK (on_clients1_activate),
                    NULL);
  g_signal_connect ((gpointer) mi_order1, "activate",
                    G_CALLBACK (on_order1_activate),
                    NULL);
  g_signal_connect ((gpointer) mi_stock1, "activate",
                    G_CALLBACK (on_stock1_activate),
                    NULL);
  g_signal_connect ((gpointer) mi_dms1, "activate",
                    G_CALLBACK (on_dms1_activate),
                    NULL);
  g_signal_connect ((gpointer) mi_cash_account_book1, "activate",
                    G_CALLBACK (on_cash_account_book1_activate),
                    NULL);
  g_signal_connect ((gpointer) mi_test1, "activate",
                    G_CALLBACK (on_test1_activate),
                    NULL);
  g_signal_connect ((gpointer) mi_expert_system1, "activate",
                    G_CALLBACK (on_expert_system1_activate),
                    NULL);
  g_signal_connect ((gpointer) mi_project1, "activate",
                    G_CALLBACK (on_project1_activate),
                    NULL);
  g_signal_connect ((gpointer) preferences1, "activate",
                    G_CALLBACK (on_preferences1_activate),
                    NULL);
  g_signal_connect ((gpointer) mi_user1, "activate",
                    G_CALLBACK (on_pref_user1_activate),
                    NULL);
  g_signal_connect ((gpointer) mi_finances1, "activate",
                    G_CALLBACK (on_prefs_finances_activate),
                    NULL);
  g_signal_connect ((gpointer) update1, "activate",
                    G_CALLBACK (on_update1_activate),
                    NULL);
  g_signal_connect ((gpointer) mi_report_generator1, "activate",
                    G_CALLBACK (on_report_generator1_activate),
                    NULL);
  g_signal_connect ((gpointer) mi_webshop1, "activate",
                    G_CALLBACK (on_webshop1_activate),
                    NULL);
  g_signal_connect ((gpointer) databases1, "activate",
                    G_CALLBACK (on_databases1_activate),
                    NULL);
  g_signal_connect ((gpointer) mi_import_data1, "activate",
                    G_CALLBACK (on_import_data1_activate),
                    NULL);
  g_signal_connect ((gpointer) about1, "activate",
                    G_CALLBACK (on_about1_activate),
                    NULL);
  g_signal_connect ((gpointer) onlinehelp, "activate",
                    G_CALLBACK (on_onlinehelp_activate),
                    NULL);
  g_signal_connect ((gpointer) eUserName, "changed",
                    G_CALLBACK (on_eUserName_changed),
                    NULL);
  g_signal_connect ((gpointer) eServer, "changed",
                    G_CALLBACK (on_eUserName_changed),
                    NULL);

  /* Store pointers to all widgets, for use by lookup_widget(). */
  GLADE_HOOKUP_OBJECT_NO_REF (window1, window1, "window1");
  GLADE_HOOKUP_OBJECT (window1, vbox1, "vbox1");
  GLADE_HOOKUP_OBJECT (window1, menubar1, "menubar1");
  GLADE_HOOKUP_OBJECT (window1, connect1, "connect1");
  GLADE_HOOKUP_OBJECT (window1, connect1_menu, "connect1_menu");
  GLADE_HOOKUP_OBJECT (window1, login1, "login1");
  GLADE_HOOKUP_OBJECT (window1, logout1, "logout1");
  GLADE_HOOKUP_OBJECT (window1, trennlinie1, "trennlinie1");
  GLADE_HOOKUP_OBJECT (window1, end1, "end1");
  GLADE_HOOKUP_OBJECT (window1, image8, "image8");
  GLADE_HOOKUP_OBJECT (window1, data, "data");
  GLADE_HOOKUP_OBJECT (window1, data_menu, "data_menu");
  GLADE_HOOKUP_OBJECT (window1, mi_addresses1, "mi_addresses1");
  GLADE_HOOKUP_OBJECT (window1, mi_articles1, "mi_articles1");
  GLADE_HOOKUP_OBJECT (window1, bank1, "bank1");
  GLADE_HOOKUP_OBJECT (window1, trennlinie3, "trennlinie3");
  GLADE_HOOKUP_OBJECT (window1, mi_bibliographic, "mi_bibliographic");
  GLADE_HOOKUP_OBJECT (window1, mi_staff1, "mi_staff1");
  GLADE_HOOKUP_OBJECT (window1, trennlinie4, "trennlinie4");
  GLADE_HOOKUP_OBJECT (window1, contracts1, "contracts1");
  GLADE_HOOKUP_OBJECT (window1, contracts1_menu, "contracts1_menu");
  GLADE_HOOKUP_OBJECT (window1, mi_insurances1, "mi_insurances1");
  GLADE_HOOKUP_OBJECT (window1, mi_rent1, "mi_rent1");
  GLADE_HOOKUP_OBJECT (window1, mi_leasing1, "mi_leasing1");
  GLADE_HOOKUP_OBJECT (window1, separator3, "separator3");
  GLADE_HOOKUP_OBJECT (window1, mi_clients1, "mi_clients1");
  GLADE_HOOKUP_OBJECT (window1, action1, "action1");
  GLADE_HOOKUP_OBJECT (window1, action1_menu, "action1_menu");
  GLADE_HOOKUP_OBJECT (window1, mi_order1, "mi_order1");
  GLADE_HOOKUP_OBJECT (window1, mi_stock1, "mi_stock1");
  GLADE_HOOKUP_OBJECT (window1, mi_dms1, "mi_dms1");
  GLADE_HOOKUP_OBJECT (window1, accounting1, "accounting1");
  GLADE_HOOKUP_OBJECT (window1, accounting1_menu, "accounting1_menu");
  GLADE_HOOKUP_OBJECT (window1, mi_cash_account_book1, "mi_cash_account_book1");
  GLADE_HOOKUP_OBJECT (window1, extras, "extras");
  GLADE_HOOKUP_OBJECT (window1, extras_menu, "extras_menu");
  GLADE_HOOKUP_OBJECT (window1, mayavi1, "mayavi1");
  GLADE_HOOKUP_OBJECT (window1, mayavi1_menu, "mayavi1_menu");
  GLADE_HOOKUP_OBJECT (window1, mi_test1, "mi_test1");
  GLADE_HOOKUP_OBJECT (window1, mi_expert_system1, "mi_expert_system1");
  GLADE_HOOKUP_OBJECT (window1, mi_project1, "mi_project1");
  GLADE_HOOKUP_OBJECT (window1, trennlinie5, "trennlinie5");
  GLADE_HOOKUP_OBJECT (window1, tools, "tools");
  GLADE_HOOKUP_OBJECT (window1, tools_menu, "tools_menu");
  GLADE_HOOKUP_OBJECT (window1, preferences1, "preferences1");
  GLADE_HOOKUP_OBJECT (window1, preferences1_menu, "preferences1_menu");
  GLADE_HOOKUP_OBJECT (window1, mi_user1, "mi_user1");
  GLADE_HOOKUP_OBJECT (window1, mi_finances1, "mi_finances1");
  GLADE_HOOKUP_OBJECT (window1, update1, "update1");
  GLADE_HOOKUP_OBJECT (window1, mi_report_generator1, "mi_report_generator1");
  GLADE_HOOKUP_OBJECT (window1, mi_webshop1, "mi_webshop1");
  GLADE_HOOKUP_OBJECT (window1, separator1, "separator1");
  GLADE_HOOKUP_OBJECT (window1, databases1, "databases1");
  GLADE_HOOKUP_OBJECT (window1, trennlinie2, "trennlinie2");
  GLADE_HOOKUP_OBJECT (window1, mi_import_data1, "mi_import_data1");
  GLADE_HOOKUP_OBJECT (window1, help1, "help1");
  GLADE_HOOKUP_OBJECT (window1, help1_menu, "help1_menu");
  GLADE_HOOKUP_OBJECT (window1, about1, "about1");
  GLADE_HOOKUP_OBJECT (window1, onlinehelp, "onlinehelp");
  GLADE_HOOKUP_OBJECT (window1, table1, "table1");
  GLADE_HOOKUP_OBJECT (window1, label1, "label1");
  GLADE_HOOKUP_OBJECT (window1, eUserName, "eUserName");
  GLADE_HOOKUP_OBJECT (window1, label2, "label2");
  GLADE_HOOKUP_OBJECT (window1, eServer, "eServer");
  GLADE_HOOKUP_OBJECT (window1, label3, "label3");
  GLADE_HOOKUP_OBJECT (window1, eAppServer, "eAppServer");
  GLADE_HOOKUP_OBJECT (window1, label4, "label4");
  GLADE_HOOKUP_OBJECT (window1, eDatabase, "eDatabase");
  GLADE_HOOKUP_OBJECT (window1, label5, "label5");
  GLADE_HOOKUP_OBJECT (window1, eWebshop, "eWebshop");
  GLADE_HOOKUP_OBJECT (window1, hbox1, "hbox1");
  GLADE_HOOKUP_OBJECT (window1, scrolledwindow3, "scrolledwindow3");
  GLADE_HOOKUP_OBJECT (window1, tree1, "tree1");
  GLADE_HOOKUP_OBJECT (window1, vbox3, "vbox3");
  GLADE_HOOKUP_OBJECT (window1, scrolledwindow4, "scrolledwindow4");
  GLADE_HOOKUP_OBJECT (window1, tvEvents, "tvEvents");
  GLADE_HOOKUP_OBJECT (window1, calendar1, "calendar1");
  GLADE_HOOKUP_OBJECT_NO_REF (window1, tooltips, "tooltips");

  return window1;
}

GtkWidget*
create_aCuon (void)
{
  GtkWidget *aCuon;
  GtkWidget *dialog_vbox1;
  GtkWidget *vbox2;
  GtkWidget *label6;
  GtkWidget *label7;
  GtkWidget *scrolledwindow1;
  GtkWidget *textview3;
  GtkWidget *scrolledwindow2;
  GtkWidget *textview2;
  GtkWidget *About_Version;
  GtkWidget *dialog_action_area1;
  GtkWidget *okAbout1;

  aCuon = gtk_dialog_new ();
  gtk_window_set_title (GTK_WINDOW (aCuon), _("About CUON"));
  gtk_window_set_type_hint (GTK_WINDOW (aCuon), GDK_WINDOW_TYPE_HINT_DIALOG);

  dialog_vbox1 = GTK_DIALOG (aCuon)->vbox;
  gtk_widget_show (dialog_vbox1);
  gtk_widget_set_size_request (dialog_vbox1, 297, 253);

  vbox2 = gtk_vbox_new (FALSE, 0);
  gtk_widget_show (vbox2);
  gtk_box_pack_start (GTK_BOX (dialog_vbox1), vbox2, TRUE, TRUE, 0);

  label6 = gtk_label_new (_("C.U.O.N."));
  gtk_widget_show (label6);
  gtk_box_pack_start (GTK_BOX (vbox2), label6, FALSE, FALSE, 0);

  label7 = gtk_label_new (_("An Internet Business-Software"));
  gtk_widget_show (label7);
  gtk_box_pack_start (GTK_BOX (vbox2), label7, FALSE, FALSE, 0);

  scrolledwindow1 = gtk_scrolled_window_new (NULL, NULL);
  gtk_widget_show (scrolledwindow1);
  gtk_box_pack_start (GTK_BOX (vbox2), scrolledwindow1, TRUE, TRUE, 0);
  gtk_scrolled_window_set_shadow_type (GTK_SCROLLED_WINDOW (scrolledwindow1), GTK_SHADOW_IN);

  textview3 = gtk_text_view_new ();
  gtk_widget_show (textview3);
  gtk_container_add (GTK_CONTAINER (scrolledwindow1), textview3);

  scrolledwindow2 = gtk_scrolled_window_new (NULL, NULL);
  gtk_widget_show (scrolledwindow2);
  gtk_box_pack_start (GTK_BOX (dialog_vbox1), scrolledwindow2, TRUE, TRUE, 0);
  gtk_scrolled_window_set_shadow_type (GTK_SCROLLED_WINDOW (scrolledwindow2), GTK_SHADOW_IN);

  textview2 = gtk_text_view_new ();
  gtk_widget_show (textview2);
  gtk_container_add (GTK_CONTAINER (scrolledwindow2), textview2);
  gtk_text_buffer_set_text (gtk_text_view_get_buffer (GTK_TEXT_VIEW (textview2)), _("Authors:\nJuergen Hamel, 32584 Loehne, Germany"), -1);

  About_Version = gtk_label_new ("");
  gtk_widget_show (About_Version);
  gtk_box_pack_start (GTK_BOX (dialog_vbox1), About_Version, FALSE, FALSE, 0);

  dialog_action_area1 = GTK_DIALOG (aCuon)->action_area;
  gtk_widget_show (dialog_action_area1);
  gtk_button_box_set_layout (GTK_BUTTON_BOX (dialog_action_area1), GTK_BUTTONBOX_SPREAD);

  okAbout1 = gtk_button_new_from_stock ("gtk-ok");
  gtk_widget_show (okAbout1);
  gtk_dialog_add_action_widget (GTK_DIALOG (aCuon), okAbout1, GTK_RESPONSE_OK);
  gtk_container_set_border_width (GTK_CONTAINER (okAbout1), 2);
  GTK_WIDGET_SET_FLAGS (okAbout1, GTK_CAN_DEFAULT);

  g_signal_connect ((gpointer) okAbout1, "clicked",
                    G_CALLBACK (on_okAbout1_clicked),
                    NULL);

  /* Store pointers to all widgets, for use by lookup_widget(). */
  GLADE_HOOKUP_OBJECT_NO_REF (aCuon, aCuon, "aCuon");
  GLADE_HOOKUP_OBJECT_NO_REF (aCuon, dialog_vbox1, "dialog_vbox1");
  GLADE_HOOKUP_OBJECT (aCuon, vbox2, "vbox2");
  GLADE_HOOKUP_OBJECT (aCuon, label6, "label6");
  GLADE_HOOKUP_OBJECT (aCuon, label7, "label7");
  GLADE_HOOKUP_OBJECT (aCuon, scrolledwindow1, "scrolledwindow1");
  GLADE_HOOKUP_OBJECT (aCuon, textview3, "textview3");
  GLADE_HOOKUP_OBJECT (aCuon, scrolledwindow2, "scrolledwindow2");
  GLADE_HOOKUP_OBJECT (aCuon, textview2, "textview2");
  GLADE_HOOKUP_OBJECT (aCuon, About_Version, "About_Version");
  GLADE_HOOKUP_OBJECT_NO_REF (aCuon, dialog_action_area1, "dialog_action_area1");
  GLADE_HOOKUP_OBJECT (aCuon, okAbout1, "okAbout1");

  return aCuon;
}

