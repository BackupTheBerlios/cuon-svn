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

#include <bonobo.h>
#include <gnome.h>

#include "callbacks.h"
#include "interface.h"
#include "support.h"

#define GLADE_HOOKUP_OBJECT(component,widget,name) \
  g_object_set_data_full (G_OBJECT (component), name, \
    gtk_widget_ref (widget), (GDestroyNotify) gtk_widget_unref)

#define GLADE_HOOKUP_OBJECT_NO_REF(component,widget,name) \
  g_object_set_data (G_OBJECT (component), name, widget)

static GnomeUIInfo sql_server1_menu_uiinfo[] =
{
  {
    GNOME_APP_UI_ITEM, N_("db_check"),
    NULL,
    (gpointer) on_dbcheck1_activate, NULL, NULL,
    GNOME_APP_PIXMAP_NONE, NULL,
    0, (GdkModifierType) 0, NULL
  },
  {
    GNOME_APP_UI_ITEM, N_("trigger"),
    NULL,
    (gpointer) on_trigger1_activate, NULL, NULL,
    GNOME_APP_PIXMAP_NONE, NULL,
    0, (GdkModifierType) 0, NULL
  },
  {
    GNOME_APP_UI_ITEM, N_("grants"),
    N_("set groups, user and grants to sql-server"),
    (gpointer) on_grants1_activate, NULL, NULL,
    GNOME_APP_PIXMAP_NONE, NULL,
    0, (GdkModifierType) 0, NULL
  },
  {
    GNOME_APP_UI_ITEM, N_("table import"),
    NULL,
    (gpointer) on_table_import1_activate, NULL, NULL,
    GNOME_APP_PIXMAP_NONE, NULL,
    0, (GdkModifierType) 0, NULL
  },
  GNOMEUIINFO_SEPARATOR,
  {
    GNOME_APP_UI_ITEM, N_("Close"),
    NULL,
    (gpointer) on_close1_activate, NULL, NULL,
    GNOME_APP_PIXMAP_NONE, NULL,
    0, (GdkModifierType) 0, NULL
  },
  GNOMEUIINFO_END
};

static GnomeUIInfo xml_tools1_menu_uiinfo[] =
{
  {
    GNOME_APP_UI_ITEM, N_("load Defaults"),
    NULL,
    (gpointer) on_load_defaults1_activate, NULL, NULL,
    GNOME_APP_PIXMAP_NONE, NULL,
    0, (GdkModifierType) 0, NULL
  },
  GNOMEUIINFO_END
};

static GnomeUIInfo export1_menu_uiinfo[] =
{
  {
    GNOME_APP_UI_ITEM, N_("LDAP"),
    NULL,
    (gpointer) on_ldap1_activate, NULL, NULL,
    GNOME_APP_PIXMAP_NONE, NULL,
    0, (GdkModifierType) 0, NULL
  },
  {
    GNOME_APP_UI_ITEM, N_("php_groupware"),
    NULL,
    (gpointer) on_php_groupware1_activate, NULL, NULL,
    GNOME_APP_PIXMAP_NONE, NULL,
    0, (GdkModifierType) 0, NULL
  },
  GNOMEUIINFO_END
};

static GnomeUIInfo import1_menu_uiinfo[] =
{
  {
    GNOME_APP_UI_ITEM, N_("php_groupware"),
    NULL,
    (gpointer) on_php_groupware2_activate, NULL, NULL,
    GNOME_APP_PIXMAP_NONE, NULL,
    0, (GdkModifierType) 0, NULL
  },
  {
    GNOME_APP_UI_ITEM, N_("Zipcode"),
    NULL,
    (gpointer) on_import_zipcode1_activate, NULL, NULL,
    GNOME_APP_PIXMAP_NONE, NULL,
    0, (GdkModifierType) 0, NULL
  },
  GNOMEUIINFO_END
};

static GnomeUIInfo menubar1_uiinfo[] =
{
  {
    GNOME_APP_UI_SUBTREE, N_("SQL-Server"),
    NULL,
    sql_server1_menu_uiinfo, NULL, NULL,
    GNOME_APP_PIXMAP_NONE, NULL,
    0, (GdkModifierType) 0, NULL
  },
  {
    GNOME_APP_UI_SUBTREE, N_("XML-Tools"),
    NULL,
    xml_tools1_menu_uiinfo, NULL, NULL,
    GNOME_APP_PIXMAP_NONE, NULL,
    0, (GdkModifierType) 0, NULL
  },
  {
    GNOME_APP_UI_SUBTREE, N_("Export"),
    NULL,
    export1_menu_uiinfo, NULL, NULL,
    GNOME_APP_PIXMAP_NONE, NULL,
    0, (GdkModifierType) 0, NULL
  },
  {
    GNOME_APP_UI_SUBTREE, N_("Import"),
    NULL,
    import1_menu_uiinfo, NULL, NULL,
    GNOME_APP_PIXMAP_NONE, NULL,
    0, (GdkModifierType) 0, NULL
  },
  GNOMEUIINFO_END
};

GtkWidget*
create_DatabasesMainwindow (void)
{
  GtkWidget *DatabasesMainwindow;
  GtkWidget *vbox1;
  GtkWidget *menubar1;

  DatabasesMainwindow = gtk_window_new (GTK_WINDOW_TOPLEVEL);
  gtk_window_set_title (GTK_WINDOW (DatabasesMainwindow), _("Datenbanken"));
  gtk_window_set_default_size (GTK_WINDOW (DatabasesMainwindow), 369, 135);

  vbox1 = gtk_vbox_new (FALSE, 0);
  gtk_widget_show (vbox1);
  gtk_container_add (GTK_CONTAINER (DatabasesMainwindow), vbox1);

  menubar1 = gtk_menu_bar_new ();
  gtk_widget_show (menubar1);
  gtk_box_pack_start (GTK_BOX (vbox1), menubar1, FALSE, FALSE, 0);
  gnome_app_fill_menu (GTK_MENU_SHELL (menubar1), menubar1_uiinfo,
                       NULL, FALSE, 0);

  /* Store pointers to all widgets, for use by lookup_widget(). */
  GLADE_HOOKUP_OBJECT_NO_REF (DatabasesMainwindow, DatabasesMainwindow, "DatabasesMainwindow");
  GLADE_HOOKUP_OBJECT (DatabasesMainwindow, vbox1, "vbox1");
  GLADE_HOOKUP_OBJECT (DatabasesMainwindow, menubar1, "menubar1");
  GLADE_HOOKUP_OBJECT (DatabasesMainwindow, menubar1_uiinfo[0].widget, "sql_server1");
  GLADE_HOOKUP_OBJECT (DatabasesMainwindow, sql_server1_menu_uiinfo[0].widget, "dbcheck1");
  GLADE_HOOKUP_OBJECT (DatabasesMainwindow, sql_server1_menu_uiinfo[1].widget, "trigger1");
  GLADE_HOOKUP_OBJECT (DatabasesMainwindow, sql_server1_menu_uiinfo[2].widget, "grants1");
  GLADE_HOOKUP_OBJECT (DatabasesMainwindow, sql_server1_menu_uiinfo[3].widget, "table_import1");
  GLADE_HOOKUP_OBJECT (DatabasesMainwindow, sql_server1_menu_uiinfo[4].widget, "trennlinie1");
  GLADE_HOOKUP_OBJECT (DatabasesMainwindow, sql_server1_menu_uiinfo[5].widget, "close1");
  GLADE_HOOKUP_OBJECT (DatabasesMainwindow, menubar1_uiinfo[1].widget, "xml_tools1");
  GLADE_HOOKUP_OBJECT (DatabasesMainwindow, xml_tools1_menu_uiinfo[0].widget, "load_defaults1");
  GLADE_HOOKUP_OBJECT (DatabasesMainwindow, menubar1_uiinfo[2].widget, "export1");
  GLADE_HOOKUP_OBJECT (DatabasesMainwindow, export1_menu_uiinfo[0].widget, "ldap1");
  GLADE_HOOKUP_OBJECT (DatabasesMainwindow, export1_menu_uiinfo[1].widget, "php_groupware1");
  GLADE_HOOKUP_OBJECT (DatabasesMainwindow, menubar1_uiinfo[3].widget, "import1");
  GLADE_HOOKUP_OBJECT (DatabasesMainwindow, import1_menu_uiinfo[0].widget, "php_groupware2");
  GLADE_HOOKUP_OBJECT (DatabasesMainwindow, import1_menu_uiinfo[1].widget, "zipcode1");

  return DatabasesMainwindow;
}

GtkWidget*
create_tableImportSQLStructure (void)
{
  GtkWidget *tableImportSQLStructure;
  GtkWidget *table1;
  GtkWidget *lExistTable;
  GtkWidget *vbox2;
  GtkWidget *rStandard;
  GSList *rStandard_group = NULL;
  GtkWidget *rExt1;
  GSList *rExt1_group = NULL;
  GtkWidget *rExt2;
  GSList *rExt2_group = NULL;
  GtkWidget *lDatabase;
  GtkWidget *bCancel;
  GtkWidget *bOK;
  GtkWidget *scrolledwindow1;
  GtkWidget *viewport1;
  GtkWidget *tree1;

  tableImportSQLStructure = gtk_window_new (GTK_WINDOW_TOPLEVEL);
  gtk_window_set_title (GTK_WINDOW (tableImportSQLStructure), _("Tabelellen-Struktur importieren"));

  table1 = gtk_table_new (3, 2, FALSE);
  gtk_widget_show (table1);
  gtk_container_add (GTK_CONTAINER (tableImportSQLStructure), table1);

  lExistTable = gtk_label_new (_("Existierende Tabellen"));
  gtk_widget_show (lExistTable);
  gtk_table_attach (GTK_TABLE (table1), lExistTable, 0, 1, 0, 1,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_label_set_justify (GTK_LABEL (lExistTable), GTK_JUSTIFY_CENTER);
  gtk_misc_set_alignment (GTK_MISC (lExistTable), 0, 0.5);

  vbox2 = gtk_vbox_new (FALSE, 0);
  gtk_widget_show (vbox2);
  gtk_table_attach (GTK_TABLE (table1), vbox2, 1, 2, 1, 2,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (GTK_FILL), 0, 0);

  rStandard = gtk_radio_button_new_with_mnemonic (NULL, _("Standard"));
  gtk_widget_show (rStandard);
  gtk_box_pack_start (GTK_BOX (vbox2), rStandard, FALSE, FALSE, 0);
  gtk_radio_button_set_group (GTK_RADIO_BUTTON (rStandard), rStandard_group);
  rStandard_group = gtk_radio_button_get_group (GTK_RADIO_BUTTON (rStandard));

  rExt1 = gtk_radio_button_new_with_mnemonic (NULL, _("Extended 1"));
  gtk_widget_show (rExt1);
  gtk_box_pack_start (GTK_BOX (vbox2), rExt1, FALSE, FALSE, 0);
  gtk_radio_button_set_group (GTK_RADIO_BUTTON (rExt1), rExt1_group);
  rExt1_group = gtk_radio_button_get_group (GTK_RADIO_BUTTON (rExt1));

  rExt2 = gtk_radio_button_new_with_mnemonic (NULL, _("Extendet 2"));
  gtk_widget_show (rExt2);
  gtk_box_pack_start (GTK_BOX (vbox2), rExt2, FALSE, FALSE, 0);
  gtk_radio_button_set_group (GTK_RADIO_BUTTON (rExt2), rExt2_group);
  rExt2_group = gtk_radio_button_get_group (GTK_RADIO_BUTTON (rExt2));

  lDatabase = gtk_label_new (_("Database"));
  gtk_widget_show (lDatabase);
  gtk_table_attach (GTK_TABLE (table1), lDatabase, 1, 2, 0, 1,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_label_set_justify (GTK_LABEL (lDatabase), GTK_JUSTIFY_CENTER);
  gtk_misc_set_alignment (GTK_MISC (lDatabase), 0, 0.5);

  bCancel = gtk_button_new_with_mnemonic (_("Abbruch"));
  gtk_widget_show (bCancel);
  gtk_table_attach (GTK_TABLE (table1), bCancel, 1, 2, 2, 3,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);

  bOK = gtk_button_new_with_mnemonic (_("O.K."));
  gtk_widget_show (bOK);
  gtk_table_attach (GTK_TABLE (table1), bOK, 0, 1, 2, 3,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);

  scrolledwindow1 = gtk_scrolled_window_new (NULL, NULL);
  gtk_widget_show (scrolledwindow1);
  gtk_table_attach (GTK_TABLE (table1), scrolledwindow1, 0, 1, 1, 2,
                    (GtkAttachOptions) (GTK_EXPAND | GTK_FILL),
                    (GtkAttachOptions) (GTK_EXPAND | GTK_FILL), 0, 0);
  GTK_WIDGET_UNSET_FLAGS (scrolledwindow1, GTK_CAN_FOCUS);

  viewport1 = gtk_viewport_new (NULL, NULL);
  gtk_widget_show (viewport1);
  gtk_container_add (GTK_CONTAINER (scrolledwindow1), viewport1);

  tree1 = gtk_tree_view_new ();
  gtk_widget_show (tree1);
  gtk_container_add (GTK_CONTAINER (viewport1), tree1);
  GTK_WIDGET_UNSET_FLAGS (tree1, GTK_CAN_FOCUS);

  g_signal_connect ((gpointer) rStandard, "clicked",
                    G_CALLBACK (on_rStandard_clicked),
                    NULL);
  g_signal_connect ((gpointer) rExt1, "clicked",
                    G_CALLBACK (on_rExt1_clicked),
                    NULL);
  g_signal_connect ((gpointer) rExt2, "clicked",
                    G_CALLBACK (on_rExt2_clicked),
                    NULL);
  g_signal_connect ((gpointer) bCancel, "clicked",
                    G_CALLBACK (on_bCancel_clicked),
                    NULL);
  g_signal_connect ((gpointer) bOK, "clicked",
                    G_CALLBACK (on_bOK_clicked),
                    NULL);

  /* Store pointers to all widgets, for use by lookup_widget(). */
  GLADE_HOOKUP_OBJECT_NO_REF (tableImportSQLStructure, tableImportSQLStructure, "tableImportSQLStructure");
  GLADE_HOOKUP_OBJECT (tableImportSQLStructure, table1, "table1");
  GLADE_HOOKUP_OBJECT (tableImportSQLStructure, lExistTable, "lExistTable");
  GLADE_HOOKUP_OBJECT (tableImportSQLStructure, vbox2, "vbox2");
  GLADE_HOOKUP_OBJECT (tableImportSQLStructure, rStandard, "rStandard");
  GLADE_HOOKUP_OBJECT (tableImportSQLStructure, rExt1, "rExt1");
  GLADE_HOOKUP_OBJECT (tableImportSQLStructure, rExt2, "rExt2");
  GLADE_HOOKUP_OBJECT (tableImportSQLStructure, lDatabase, "lDatabase");
  GLADE_HOOKUP_OBJECT (tableImportSQLStructure, bCancel, "bCancel");
  GLADE_HOOKUP_OBJECT (tableImportSQLStructure, bOK, "bOK");
  GLADE_HOOKUP_OBJECT (tableImportSQLStructure, scrolledwindow1, "scrolledwindow1");
  GLADE_HOOKUP_OBJECT (tableImportSQLStructure, viewport1, "viewport1");
  GLADE_HOOKUP_OBJECT (tableImportSQLStructure, tree1, "tree1");

  return tableImportSQLStructure;
}

GtkWidget*
create_zip_fileselection1 (void)
{
  GtkWidget *zip_fileselection1;
  GtkWidget *ok_button1;
  GtkWidget *cancel_button1;

  zip_fileselection1 = gtk_file_selection_new (_("choose file"));
  gtk_container_set_border_width (GTK_CONTAINER (zip_fileselection1), 10);
  GTK_WINDOW (zip_fileselection1)->type = GTK_WINDOW_POPUP;
  gtk_window_set_position (GTK_WINDOW (zip_fileselection1), GTK_WIN_POS_CENTER);

  ok_button1 = GTK_FILE_SELECTION (zip_fileselection1)->ok_button;
  gtk_widget_show (ok_button1);
  GTK_WIDGET_SET_FLAGS (ok_button1, GTK_CAN_DEFAULT);

  cancel_button1 = GTK_FILE_SELECTION (zip_fileselection1)->cancel_button;
  gtk_widget_show (cancel_button1);
  GTK_WIDGET_SET_FLAGS (cancel_button1, GTK_CAN_DEFAULT);

  g_signal_connect ((gpointer) ok_button1, "clicked",
                    G_CALLBACK (on_fd_ok_button1_clicked),
                    NULL);
  g_signal_connect ((gpointer) cancel_button1, "clicked",
                    G_CALLBACK (on_fd_cancel_button1_clicked),
                    NULL);

  /* Store pointers to all widgets, for use by lookup_widget(). */
  GLADE_HOOKUP_OBJECT_NO_REF (zip_fileselection1, zip_fileselection1, "zip_fileselection1");
  GLADE_HOOKUP_OBJECT_NO_REF (zip_fileselection1, ok_button1, "ok_button1");
  GLADE_HOOKUP_OBJECT_NO_REF (zip_fileselection1, cancel_button1, "cancel_button1");

  return zip_fileselection1;
}

