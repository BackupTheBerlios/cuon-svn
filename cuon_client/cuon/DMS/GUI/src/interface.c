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

static GnomeUIInfo file1_menu_uiinfo[] =
{
  {
    GNOME_APP_UI_ITEM, N_("Print S_etup..."),
    NULL,
    (gpointer) on_choosePrinter1_activate, NULL, NULL,
    GNOME_APP_PIXMAP_NONE, NULL,
    0, (GdkModifierType) 0, NULL
  },
  GNOMEUIINFO_SEPARATOR,
  GNOMEUIINFO_MENU_CLOSE_ITEM (on_quit1_activate, NULL),
  GNOMEUIINFO_END
};

static GnomeUIInfo profile1_menu_uiinfo[] =
{
  {
    GNOME_APP_UI_ITEM, N_("New"),
    NULL,
    (gpointer) on_new1_activate, NULL, NULL,
    GNOME_APP_PIXMAP_NONE, NULL,
    0, (GdkModifierType) 0, NULL
  },
  {
    GNOME_APP_UI_ITEM, N_("Edit"),
    NULL,
    (gpointer) on_edit1_activate, NULL, NULL,
    GNOME_APP_PIXMAP_NONE, NULL,
    0, (GdkModifierType) 0, NULL
  },
  {
    GNOME_APP_UI_ITEM, N_("Save"),
    NULL,
    (gpointer) on_save1_activate, NULL, NULL,
    GNOME_APP_PIXMAP_NONE, NULL,
    0, (GdkModifierType) 0, NULL
  },
  GNOMEUIINFO_SEPARATOR,
  {
    GNOME_APP_UI_ITEM, N_("print"),
    NULL,
    (gpointer) on_print1_activate, NULL, NULL,
    GNOME_APP_PIXMAP_NONE, NULL,
    0, (GdkModifierType) 0, NULL
  },
  GNOMEUIINFO_SEPARATOR,
  {
    GNOME_APP_UI_ITEM, N_("clear"),
    NULL,
    (gpointer) on_clear1_activate, NULL, NULL,
    GNOME_APP_PIXMAP_NONE, NULL,
    0, (GdkModifierType) 0, NULL
  },
  GNOMEUIINFO_END
};

static GnomeUIInfo menubar1_uiinfo[] =
{
  {
    GNOME_APP_UI_SUBTREE, N_("_File"),
    NULL,
    file1_menu_uiinfo, NULL, NULL,
    GNOME_APP_PIXMAP_NONE, NULL,
    0, (GdkModifierType) 0, NULL
  },
  {
    GNOME_APP_UI_SUBTREE, N_("Documents"),
    NULL,
    profile1_menu_uiinfo, NULL, NULL,
    GNOME_APP_PIXMAP_NONE, NULL,
    0, (GdkModifierType) 0, NULL
  },
  GNOMEUIINFO_END
};

GtkWidget*
create_DMSMainwindow (void)
{
  GtkWidget *DMSMainwindow;
  GtkWidget *vbox1;
  GtkWidget *alignment1;
  GtkWidget *menubar1;
  GtkWidget *toolbar1;
  GtkWidget *table5;
  GtkWidget *label31;
  GtkWidget *label32;
  GtkWidget *label33;
  GtkWidget *label34;
  GtkWidget *label35;
  GtkWidget *label36;
  GtkWidget *eSearchTitle;
  GtkWidget *eSearchSub2;
  GtkWidget *eSearchCategory;
  GtkWidget *eSearchSub3;
  GtkWidget *eSearchSub1;
  GtkWidget *eSearchSub4;
  GtkWidget *label37;
  GtkWidget *eSearchSub5;
  GtkWidget *label38;
  GtkWidget *label39;
  GtkWidget *label40;
  GtkWidget *label41;
  GtkWidget *button1;
  GtkWidget *eSearchSearch1;
  GtkWidget *eSearchSearch2;
  GtkWidget *eSearchSearch3;
  GtkWidget *eSearchSearch4;
  GtkWidget *scrolledwindow1;
  GtkWidget *viewport1;
  GtkWidget *tree1;
  GtkWidget *notebook1;
  GtkWidget *hbox2;
  GtkWidget *table2;
  GtkWidget *label16;
  GtkWidget *eTitle;
  GtkWidget *label17;
  GtkWidget *eCategory;
  GtkWidget *label23;
  GtkWidget *eSub1;
  GtkWidget *label24;
  GtkWidget *eSub2;
  GtkWidget *label28;
  GtkWidget *label29;
  GtkWidget *label30;
  GtkWidget *eSub3;
  GtkWidget *eSub4;
  GtkWidget *eSub5;
  GtkWidget *label18;
  GtkWidget *label25;
  GtkWidget *label26;
  GtkWidget *label27;
  GtkWidget *eSearch1;
  GtkWidget *eSearch2;
  GtkWidget *eSearch3;
  GtkWidget *eSearch4;
  GtkWidget *bScan;
  GtkWidget *bOCR;
  GtkWidget *bView;
  GtkWidget *fileentry1;
  GtkWidget *eImportFile;
  GtkWidget *bImport;
  GtkWidget *iThumbnail;
  GtkWidget *lProfile;
  GtkWidget *table3;
  GtkWidget *label21;
  GtkWidget *label20;
  GtkWidget *table4;
  GtkWidget *label22;
  GtkWidget *label19;

  DMSMainwindow = gtk_window_new (GTK_WINDOW_TOPLEVEL);
  gtk_window_set_title (GTK_WINDOW (DMSMainwindow), _("Document Management System"));

  vbox1 = gtk_vbox_new (FALSE, 0);
  gtk_widget_show (vbox1);
  gtk_container_add (GTK_CONTAINER (DMSMainwindow), vbox1);

  alignment1 = gtk_alignment_new (0.5, 0.5, 1, 1);
  gtk_widget_show (alignment1);
  gtk_box_pack_start (GTK_BOX (vbox1), alignment1, FALSE, FALSE, 0);

  menubar1 = gtk_menu_bar_new ();
  gtk_widget_show (menubar1);
  gtk_container_add (GTK_CONTAINER (alignment1), menubar1);
  gnome_app_fill_menu (GTK_MENU_SHELL (menubar1), menubar1_uiinfo,
                       NULL, FALSE, 0);

  toolbar1 = gtk_toolbar_new ();
  gtk_widget_show (toolbar1);
  gtk_box_pack_start (GTK_BOX (vbox1), toolbar1, FALSE, FALSE, 0);
  gtk_toolbar_set_style (GTK_TOOLBAR (toolbar1), GTK_TOOLBAR_BOTH);

  table5 = gtk_table_new (4, 6, TRUE);
  gtk_widget_show (table5);
  gtk_box_pack_start (GTK_BOX (vbox1), table5, FALSE, TRUE, 0);

  label31 = gtk_label_new (_("Title"));
  gtk_widget_show (label31);
  gtk_table_attach (GTK_TABLE (table5), label31, 0, 1, 0, 1,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_misc_set_alignment (GTK_MISC (label31), 0, 0.5);

  label32 = gtk_label_new (_("Sub2"));
  gtk_widget_show (label32);
  gtk_table_attach (GTK_TABLE (table5), label32, 0, 1, 1, 2,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_misc_set_alignment (GTK_MISC (label32), 0, 0.5);

  label33 = gtk_label_new (_("Category"));
  gtk_widget_show (label33);
  gtk_table_attach (GTK_TABLE (table5), label33, 2, 3, 0, 1,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_misc_set_alignment (GTK_MISC (label33), 0, 0.5);

  label34 = gtk_label_new (_("Sub3"));
  gtk_widget_show (label34);
  gtk_table_attach (GTK_TABLE (table5), label34, 2, 3, 1, 2,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_misc_set_alignment (GTK_MISC (label34), 0, 0.5);

  label35 = gtk_label_new (_("Sub1"));
  gtk_widget_show (label35);
  gtk_table_attach (GTK_TABLE (table5), label35, 4, 5, 0, 1,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_misc_set_alignment (GTK_MISC (label35), 0, 0.5);

  label36 = gtk_label_new (_("Sub4"));
  gtk_widget_show (label36);
  gtk_table_attach (GTK_TABLE (table5), label36, 4, 5, 1, 2,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_misc_set_alignment (GTK_MISC (label36), 0, 0.5);

  eSearchTitle = gtk_entry_new ();
  gtk_widget_show (eSearchTitle);
  gtk_table_attach (GTK_TABLE (table5), eSearchTitle, 1, 2, 0, 1,
                    (GtkAttachOptions) (GTK_EXPAND | GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);

  eSearchSub2 = gtk_entry_new ();
  gtk_widget_show (eSearchSub2);
  gtk_table_attach (GTK_TABLE (table5), eSearchSub2, 1, 2, 1, 2,
                    (GtkAttachOptions) (GTK_EXPAND | GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);

  eSearchCategory = gtk_entry_new ();
  gtk_widget_show (eSearchCategory);
  gtk_table_attach (GTK_TABLE (table5), eSearchCategory, 3, 4, 0, 1,
                    (GtkAttachOptions) (GTK_EXPAND | GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);

  eSearchSub3 = gtk_entry_new ();
  gtk_widget_show (eSearchSub3);
  gtk_table_attach (GTK_TABLE (table5), eSearchSub3, 3, 4, 1, 2,
                    (GtkAttachOptions) (GTK_EXPAND | GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);

  eSearchSub1 = gtk_entry_new ();
  gtk_widget_show (eSearchSub1);
  gtk_table_attach (GTK_TABLE (table5), eSearchSub1, 5, 6, 0, 1,
                    (GtkAttachOptions) (GTK_EXPAND | GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);

  eSearchSub4 = gtk_entry_new ();
  gtk_widget_show (eSearchSub4);
  gtk_table_attach (GTK_TABLE (table5), eSearchSub4, 5, 6, 1, 2,
                    (GtkAttachOptions) (GTK_EXPAND | GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);

  label37 = gtk_label_new (_("Sub5"));
  gtk_widget_show (label37);
  gtk_table_attach (GTK_TABLE (table5), label37, 0, 1, 2, 3,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_misc_set_alignment (GTK_MISC (label37), 0, 0.5);

  eSearchSub5 = gtk_entry_new ();
  gtk_widget_show (eSearchSub5);
  gtk_table_attach (GTK_TABLE (table5), eSearchSub5, 1, 2, 2, 3,
                    (GtkAttachOptions) (GTK_EXPAND | GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);

  label38 = gtk_label_new (_("Search1"));
  gtk_widget_show (label38);
  gtk_table_attach (GTK_TABLE (table5), label38, 2, 3, 2, 3,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_misc_set_alignment (GTK_MISC (label38), 0, 0.5);

  label39 = gtk_label_new (_("Search2"));
  gtk_widget_show (label39);
  gtk_table_attach (GTK_TABLE (table5), label39, 4, 5, 2, 3,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_misc_set_alignment (GTK_MISC (label39), 0, 0.5);

  label40 = gtk_label_new (_("Search3"));
  gtk_widget_show (label40);
  gtk_table_attach (GTK_TABLE (table5), label40, 0, 1, 3, 4,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_misc_set_alignment (GTK_MISC (label40), 0, 0.5);

  label41 = gtk_label_new (_("Search4"));
  gtk_widget_show (label41);
  gtk_table_attach (GTK_TABLE (table5), label41, 2, 3, 3, 4,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_misc_set_alignment (GTK_MISC (label41), 0, 0.5);

  button1 = gtk_button_new_with_mnemonic (_("Search"));
  gtk_widget_show (button1);
  gtk_table_attach (GTK_TABLE (table5), button1, 5, 6, 3, 4,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);

  eSearchSearch1 = gtk_entry_new ();
  gtk_widget_show (eSearchSearch1);
  gtk_table_attach (GTK_TABLE (table5), eSearchSearch1, 3, 4, 2, 3,
                    (GtkAttachOptions) (GTK_EXPAND | GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);

  eSearchSearch2 = gtk_entry_new ();
  gtk_widget_show (eSearchSearch2);
  gtk_table_attach (GTK_TABLE (table5), eSearchSearch2, 5, 6, 2, 3,
                    (GtkAttachOptions) (GTK_EXPAND | GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);

  eSearchSearch3 = gtk_entry_new ();
  gtk_widget_show (eSearchSearch3);
  gtk_table_attach (GTK_TABLE (table5), eSearchSearch3, 1, 2, 3, 4,
                    (GtkAttachOptions) (GTK_EXPAND | GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);

  eSearchSearch4 = gtk_entry_new ();
  gtk_widget_show (eSearchSearch4);
  gtk_table_attach (GTK_TABLE (table5), eSearchSearch4, 3, 4, 3, 4,
                    (GtkAttachOptions) (GTK_EXPAND | GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);

  scrolledwindow1 = gtk_scrolled_window_new (NULL, NULL);
  gtk_widget_show (scrolledwindow1);
  gtk_box_pack_start (GTK_BOX (vbox1), scrolledwindow1, TRUE, TRUE, 0);
  gtk_widget_set_size_request (scrolledwindow1, -1, 164);
  GTK_WIDGET_UNSET_FLAGS (scrolledwindow1, GTK_CAN_FOCUS);

  viewport1 = gtk_viewport_new (NULL, NULL);
  gtk_widget_show (viewport1);
  gtk_container_add (GTK_CONTAINER (scrolledwindow1), viewport1);

  tree1 = gtk_tree_view_new ();
  gtk_widget_show (tree1);
  gtk_container_add (GTK_CONTAINER (viewport1), tree1);
  GTK_WIDGET_UNSET_FLAGS (tree1, GTK_CAN_FOCUS);

  notebook1 = gtk_notebook_new ();
  gtk_widget_show (notebook1);
  gtk_box_pack_start (GTK_BOX (vbox1), notebook1, TRUE, TRUE, 0);

  hbox2 = gtk_hbox_new (TRUE, 0);
  gtk_widget_show (hbox2);
  gtk_container_add (GTK_CONTAINER (notebook1), hbox2);

  table2 = gtk_table_new (11, 3, FALSE);
  gtk_widget_show (table2);
  gtk_box_pack_start (GTK_BOX (hbox2), table2, TRUE, TRUE, 0);

  label16 = gtk_label_new (_("Title"));
  gtk_widget_show (label16);
  gtk_table_attach (GTK_TABLE (table2), label16, 0, 1, 0, 1,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_misc_set_alignment (GTK_MISC (label16), 0, 0.5);

  eTitle = gtk_entry_new ();
  gtk_widget_show (eTitle);
  gtk_table_attach (GTK_TABLE (table2), eTitle, 1, 2, 0, 1,
                    (GtkAttachOptions) (GTK_EXPAND | GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);

  label17 = gtk_label_new (_("Category"));
  gtk_widget_show (label17);
  gtk_table_attach (GTK_TABLE (table2), label17, 0, 1, 1, 2,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_misc_set_alignment (GTK_MISC (label17), 0, 0.5);

  eCategory = gtk_entry_new ();
  gtk_widget_show (eCategory);
  gtk_table_attach (GTK_TABLE (table2), eCategory, 1, 2, 1, 2,
                    (GtkAttachOptions) (GTK_EXPAND | GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);

  label23 = gtk_label_new (_("Sub 1"));
  gtk_widget_show (label23);
  gtk_table_attach (GTK_TABLE (table2), label23, 0, 1, 2, 3,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_misc_set_alignment (GTK_MISC (label23), 0, 0.5);

  eSub1 = gtk_entry_new ();
  gtk_widget_show (eSub1);
  gtk_table_attach (GTK_TABLE (table2), eSub1, 1, 2, 2, 3,
                    (GtkAttachOptions) (GTK_EXPAND | GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);

  label24 = gtk_label_new (_("Sub 2"));
  gtk_widget_show (label24);
  gtk_table_attach (GTK_TABLE (table2), label24, 0, 1, 3, 4,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_misc_set_alignment (GTK_MISC (label24), 0, 0.5);

  eSub2 = gtk_entry_new ();
  gtk_widget_show (eSub2);
  gtk_table_attach (GTK_TABLE (table2), eSub2, 1, 2, 3, 4,
                    (GtkAttachOptions) (GTK_EXPAND | GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);

  label28 = gtk_label_new (_("Sub 3"));
  gtk_widget_show (label28);
  gtk_table_attach (GTK_TABLE (table2), label28, 0, 1, 4, 5,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_misc_set_alignment (GTK_MISC (label28), 0, 0.5);

  label29 = gtk_label_new (_("Sub 4"));
  gtk_widget_show (label29);
  gtk_table_attach (GTK_TABLE (table2), label29, 0, 1, 5, 6,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_misc_set_alignment (GTK_MISC (label29), 0, 0.5);

  label30 = gtk_label_new (_("Sub 5"));
  gtk_widget_show (label30);
  gtk_table_attach (GTK_TABLE (table2), label30, 0, 1, 6, 7,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_misc_set_alignment (GTK_MISC (label30), 0, 0.5);

  eSub3 = gtk_entry_new ();
  gtk_widget_show (eSub3);
  gtk_table_attach (GTK_TABLE (table2), eSub3, 1, 2, 4, 5,
                    (GtkAttachOptions) (GTK_EXPAND | GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);

  eSub4 = gtk_entry_new ();
  gtk_widget_show (eSub4);
  gtk_table_attach (GTK_TABLE (table2), eSub4, 1, 2, 5, 6,
                    (GtkAttachOptions) (GTK_EXPAND | GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);

  eSub5 = gtk_entry_new ();
  gtk_widget_show (eSub5);
  gtk_table_attach (GTK_TABLE (table2), eSub5, 1, 2, 6, 7,
                    (GtkAttachOptions) (GTK_EXPAND | GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);

  label18 = gtk_label_new (_("Search 1"));
  gtk_widget_show (label18);
  gtk_table_attach (GTK_TABLE (table2), label18, 0, 1, 7, 8,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_misc_set_alignment (GTK_MISC (label18), 0, 0.5);

  label25 = gtk_label_new (_("Search 2"));
  gtk_widget_show (label25);
  gtk_table_attach (GTK_TABLE (table2), label25, 0, 1, 8, 9,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_misc_set_alignment (GTK_MISC (label25), 0, 0.5);

  label26 = gtk_label_new (_("Search 3"));
  gtk_widget_show (label26);
  gtk_table_attach (GTK_TABLE (table2), label26, 0, 1, 9, 10,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_misc_set_alignment (GTK_MISC (label26), 0, 0.5);

  label27 = gtk_label_new (_("Search 4"));
  gtk_widget_show (label27);
  gtk_table_attach (GTK_TABLE (table2), label27, 0, 1, 10, 11,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_misc_set_alignment (GTK_MISC (label27), 0, 0.5);

  eSearch1 = gtk_entry_new ();
  gtk_widget_show (eSearch1);
  gtk_table_attach (GTK_TABLE (table2), eSearch1, 1, 2, 7, 8,
                    (GtkAttachOptions) (GTK_EXPAND | GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);

  eSearch2 = gtk_entry_new ();
  gtk_widget_show (eSearch2);
  gtk_table_attach (GTK_TABLE (table2), eSearch2, 1, 2, 8, 9,
                    (GtkAttachOptions) (GTK_EXPAND | GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);

  eSearch3 = gtk_entry_new ();
  gtk_widget_show (eSearch3);
  gtk_table_attach (GTK_TABLE (table2), eSearch3, 1, 2, 9, 10,
                    (GtkAttachOptions) (GTK_EXPAND | GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);

  eSearch4 = gtk_entry_new ();
  gtk_widget_show (eSearch4);
  gtk_table_attach (GTK_TABLE (table2), eSearch4, 1, 2, 10, 11,
                    (GtkAttachOptions) (GTK_EXPAND | GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);

  bScan = gtk_button_new_with_mnemonic (_("Scan"));
  gtk_widget_show (bScan);
  gtk_table_attach (GTK_TABLE (table2), bScan, 2, 3, 0, 1,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);

  bOCR = gtk_button_new_with_mnemonic (_("OCR"));
  gtk_widget_show (bOCR);
  gtk_table_attach (GTK_TABLE (table2), bOCR, 2, 3, 1, 2,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);

  bView = gtk_button_new_with_mnemonic (_("View"));
  gtk_widget_show (bView);
  gtk_table_attach (GTK_TABLE (table2), bView, 2, 3, 10, 11,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);

  fileentry1 = gnome_file_entry_new (NULL, NULL);
  gtk_widget_show (fileentry1);
  gtk_table_attach (GTK_TABLE (table2), fileentry1, 2, 3, 2, 3,
                    (GtkAttachOptions) (GTK_EXPAND | GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);

  eImportFile = gnome_file_entry_gtk_entry (GNOME_FILE_ENTRY (fileentry1));
  gtk_widget_show (eImportFile);

  bImport = gtk_button_new_with_mnemonic (_("Import"));
  gtk_widget_show (bImport);
  gtk_table_attach (GTK_TABLE (table2), bImport, 2, 3, 3, 4,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);

  iThumbnail = create_pixmap (DMSMainwindow, NULL);
  gtk_widget_show (iThumbnail);
  gtk_box_pack_start (GTK_BOX (hbox2), iThumbnail, TRUE, TRUE, 0);
  gtk_widget_set_size_request (iThumbnail, 28, 125);

  lProfile = gtk_label_new (_("Profile"));
  gtk_widget_show (lProfile);
  gtk_notebook_set_tab_label (GTK_NOTEBOOK (notebook1), gtk_notebook_get_nth_page (GTK_NOTEBOOK (notebook1), 0), lProfile);

  table3 = gtk_table_new (3, 3, FALSE);
  gtk_widget_show (table3);
  gtk_container_add (GTK_CONTAINER (notebook1), table3);

  label21 = gtk_label_new (_("label21"));
  gtk_widget_show (label21);
  gtk_table_attach (GTK_TABLE (table3), label21, 0, 1, 0, 1,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_misc_set_alignment (GTK_MISC (label21), 0, 0.5);

  label20 = gtk_label_new (_("Related"));
  gtk_widget_show (label20);
  gtk_notebook_set_tab_label (GTK_NOTEBOOK (notebook1), gtk_notebook_get_nth_page (GTK_NOTEBOOK (notebook1), 1), label20);

  table4 = gtk_table_new (3, 4, FALSE);
  gtk_widget_show (table4);
  gtk_container_add (GTK_CONTAINER (notebook1), table4);

  label22 = gtk_label_new (_("label22"));
  gtk_widget_show (label22);
  gtk_table_attach (GTK_TABLE (table4), label22, 0, 1, 0, 1,
                    (GtkAttachOptions) (GTK_FILL),
                    (GtkAttachOptions) (0), 0, 0);
  gtk_misc_set_alignment (GTK_MISC (label22), 0, 0.5);

  label19 = gtk_label_new (_("Associated"));
  gtk_widget_show (label19);
  gtk_notebook_set_tab_label (GTK_NOTEBOOK (notebook1), gtk_notebook_get_nth_page (GTK_NOTEBOOK (notebook1), 2), label19);

  g_signal_connect ((gpointer) button1, "clicked",
                    G_CALLBACK (on_bSearch_clicked),
                    NULL);
  g_signal_connect ((gpointer) notebook1, "switch_page",
                    G_CALLBACK (on_notebook1_switch_page),
                    NULL);
  g_signal_connect ((gpointer) bScan, "clicked",
                    G_CALLBACK (on_bScan_clicked),
                    NULL);
  g_signal_connect ((gpointer) bOCR, "clicked",
                    G_CALLBACK (on_bOCR_clicked),
                    NULL);
  g_signal_connect ((gpointer) bView, "clicked",
                    G_CALLBACK (on_bView_clicked),
                    NULL);
  g_signal_connect ((gpointer) bImport, "clicked",
                    G_CALLBACK (on_bImport_clicked),
                    NULL);

  /* Store pointers to all widgets, for use by lookup_widget(). */
  GLADE_HOOKUP_OBJECT_NO_REF (DMSMainwindow, DMSMainwindow, "DMSMainwindow");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, vbox1, "vbox1");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, alignment1, "alignment1");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, menubar1, "menubar1");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, menubar1_uiinfo[0].widget, "file1");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, file1_menu_uiinfo[0].widget, "choosePrinter1");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, file1_menu_uiinfo[1].widget, "separator2");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, file1_menu_uiinfo[2].widget, "quit1");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, menubar1_uiinfo[1].widget, "profile1");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, profile1_menu_uiinfo[0].widget, "new1");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, profile1_menu_uiinfo[1].widget, "edit1");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, profile1_menu_uiinfo[2].widget, "save1");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, profile1_menu_uiinfo[3].widget, "separator3");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, profile1_menu_uiinfo[4].widget, "print1");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, profile1_menu_uiinfo[5].widget, "separator1");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, profile1_menu_uiinfo[6].widget, "clear1");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, toolbar1, "toolbar1");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, table5, "table5");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, label31, "label31");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, label32, "label32");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, label33, "label33");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, label34, "label34");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, label35, "label35");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, label36, "label36");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, eSearchTitle, "eSearchTitle");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, eSearchSub2, "eSearchSub2");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, eSearchCategory, "eSearchCategory");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, eSearchSub3, "eSearchSub3");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, eSearchSub1, "eSearchSub1");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, eSearchSub4, "eSearchSub4");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, label37, "label37");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, eSearchSub5, "eSearchSub5");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, label38, "label38");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, label39, "label39");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, label40, "label40");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, label41, "label41");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, button1, "button1");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, eSearchSearch1, "eSearchSearch1");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, eSearchSearch2, "eSearchSearch2");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, eSearchSearch3, "eSearchSearch3");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, eSearchSearch4, "eSearchSearch4");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, scrolledwindow1, "scrolledwindow1");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, viewport1, "viewport1");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, tree1, "tree1");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, notebook1, "notebook1");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, hbox2, "hbox2");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, table2, "table2");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, label16, "label16");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, eTitle, "eTitle");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, label17, "label17");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, eCategory, "eCategory");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, label23, "label23");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, eSub1, "eSub1");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, label24, "label24");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, eSub2, "eSub2");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, label28, "label28");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, label29, "label29");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, label30, "label30");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, eSub3, "eSub3");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, eSub4, "eSub4");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, eSub5, "eSub5");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, label18, "label18");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, label25, "label25");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, label26, "label26");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, label27, "label27");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, eSearch1, "eSearch1");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, eSearch2, "eSearch2");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, eSearch3, "eSearch3");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, eSearch4, "eSearch4");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, bScan, "bScan");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, bOCR, "bOCR");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, bView, "bView");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, fileentry1, "fileentry1");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, eImportFile, "eImportFile");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, bImport, "bImport");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, iThumbnail, "iThumbnail");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, lProfile, "lProfile");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, table3, "table3");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, label21, "label21");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, label20, "label20");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, table4, "table4");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, label22, "label22");
  GLADE_HOOKUP_OBJECT (DMSMainwindow, label19, "label19");

  return DMSMainwindow;
}

