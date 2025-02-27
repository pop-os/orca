# Stub file that should contain all public methods of AXUtilities
#
# Copyright 2023 Igalia, S.L.
# Author: Joanmarie Diggs <jdiggs@igalia.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., Franklin Street, Fifth Floor,
# Boston MA  02110-1301 USA.

"""
Stub file that contains all public methods of AXUtilities, including
those which are added dynamically at runtime. This is needed for type
checkers, linters, and IDEs.
"""

__id__        = "$Id$"
__version__   = "$Revision$"
__date__      = "$Date$"
__copyright__ = "Copyright (c) 2023 Igalia, S.L."
__license__   = "LGPL"

class AXUtilities:

    # From ax_utilities.py
    @staticmethod
    def get_desktop(): ...

    @staticmethod
    def get_all_applications(must_have_window=False): ...

    @staticmethod
    def is_application_in_desktop(app): ...

    @staticmethod
    def get_application_with_pid(pid): ...

    @staticmethod
    def get_all_static_text_leaf_nodes(obj): ...

    @staticmethod
    def get_all_widgets(obj, must_be_showing_and_visible=True): ...

    @staticmethod
    def get_default_button(obj): ...

    @staticmethod
    def get_focused_object(obj): ...

    @staticmethod
    def get_status_bar(obj): ...

    # From ax_utilities_role.py
    @staticmethod
    def get_dialog_roles(include_alert_as_dialog=True): ...

    @staticmethod
    def get_document_roles(): ...

    @staticmethod
    def get_form_field_roles(): ...

    @staticmethod
    def get_menu_item_roles(): ...

    @staticmethod
    def get_menu_related_roles(): ...

    @staticmethod
    def get_roles_to_exclude_from_clickables_list(): ...

    @staticmethod
    def get_set_container_roles(): ...

    @staticmethod
    def get_table_cell_roles(include_headers=True): ...

    @staticmethod
    def get_table_header_roles(): ...

    @staticmethod
    def get_table_related_roles(include_caption=False): ...

    @staticmethod
    def get_tree_related_roles(): ...

    @staticmethod
    def get_widget_roles(): ...

    @staticmethod
    def have_same_role(obj1, obj2): ...

    @staticmethod
    def is_accelerator_label(obj, role=None): ...

    @staticmethod
    def is_alert(obj, role=None): ...

    @staticmethod
    def is_animation(obj, role=None): ...

    @staticmethod
    def is_application(obj, role=None): ...

    @staticmethod
    def is_arrow(obj, role=None): ...

    @staticmethod
    def is_article(obj, role=None): ...

    @staticmethod
    def is_audio(obj, role=None): ...

    @staticmethod
    def is_autocomplete(obj, role=None): ...

    @staticmethod
    def is_block_quote(obj, role=None): ...

    @staticmethod
    def is_button(obj, role=None): ...

    @staticmethod
    def is_calendar(obj, role=None): ...

    @staticmethod
    def is_canvas(obj, role=None): ...

    @staticmethod
    def is_caption(obj, role=None): ...

    @staticmethod
    def is_chart(obj, role=None): ...

    @staticmethod
    def is_check_box(obj, role=None): ...

    @staticmethod
    def is_check_menu_item(obj, role=None): ...

    @staticmethod
    def is_color_chooser(obj, role=None): ...

    @staticmethod
    def is_column_header(obj, role=None): ...

    @staticmethod
    def is_combo_box(obj, role=None): ...

    @staticmethod
    def is_comment(obj, role=None): ...

    @staticmethod
    def is_content_deletion(obj, role=None): ...

    @staticmethod
    def is_content_insertion(obj, role=None): ...

    @staticmethod
    def is_default_button(obj, role=None): ...

    @staticmethod
    def is_date_editor(obj, role=None): ...

    @staticmethod
    def is_definition(obj, role=None): ...

    @staticmethod
    def is_description_list(obj, role=None): ...

    @staticmethod
    def is_description_term(obj, role=None): ...

    @staticmethod
    def is_description_value(obj, role=None): ...

    @staticmethod
    def is_desktop_frame(obj, role=None): ...

    @staticmethod
    def is_desktop_icon(obj, role=None): ...

    @staticmethod
    def is_dial(obj, role=None): ...

    @staticmethod
    def is_dialog(obj, role=None): ...

    @staticmethod
    def is_dialog_or_alert(obj, role=None): ...

    @staticmethod
    def is_directory_pane(obj, role=None): ...

    @staticmethod
    def is_document(obj, role=None): ...

    @staticmethod
    def is_document_email(obj, role=None): ...

    @staticmethod
    def is_document_frame(obj, role=None): ...

    @staticmethod
    def is_document_presentation(obj, role=None): ...

    @staticmethod
    def is_document_spreadsheet(obj, role=None): ...

    @staticmethod
    def is_document_text(obj, role=None): ...

    @staticmethod
    def is_document_web(obj, role=None): ...

    @staticmethod
    def is_drawing_area(obj, role=None): ...

    @staticmethod
    def is_editbar(obj, role=None): ...

    @staticmethod
    def is_embedded(obj, role=None): ...

    @staticmethod
    def is_entry(obj, role=None): ...

    @staticmethod
    def is_extended(obj, role=None): ...

    @staticmethod
    def is_file_chooser(obj, role=None): ...

    @staticmethod
    def is_filler(obj, role=None): ...

    @staticmethod
    def is_focus_traversable(obj, role=None): ...

    @staticmethod
    def is_font_chooser(obj, role=None): ...

    @staticmethod
    def is_footer(obj, role=None): ...

    @staticmethod
    def is_footnote(obj, role=None): ...

    @staticmethod
    def is_form(obj, role=None): ...

    @staticmethod
    def is_frame(obj, role=None): ...

    @staticmethod
    def is_glass_pane(obj, role=None): ...

    @staticmethod
    def is_grouping(obj, role=None): ...

    @staticmethod
    def is_header(obj, role=None): ...

    @staticmethod
    def is_heading(obj, role=None): ...

    @staticmethod
    def is_html_container(obj, role=None): ...

    @staticmethod
    def is_horizontal_scrollbar(obj, role=None): ...

    @staticmethod
    def is_horizontal_separator(obj, role=None): ...

    @staticmethod
    def is_horizontal_slider(obj, role=None): ...

    @staticmethod
    def is_icon(obj, role=None): ...

    @staticmethod
    def is_icon_or_canvas(obj, role=None): ...

    @staticmethod
    def is_image(obj, role=None): ...

    @staticmethod
    def is_image_or_canvas(obj, role=None): ...

    @staticmethod
    def is_image_map(obj, role=None): ...

    @staticmethod
    def is_info_bar(obj, role=None): ...

    @staticmethod
    def is_input_method_window(obj, role=None): ...

    @staticmethod
    def is_internal_frame(obj, role=None): ...

    @staticmethod
    def is_invalid_role(obj, role=None): ...

    @staticmethod
    def is_label(obj, role=None): ...

    @staticmethod
    def is_label_or_caption(obj, role=None): ...

    @staticmethod
    def is_landmark(obj, role=None): ...

    @staticmethod
    def is_layered_pane(obj, role=None): ...

    @staticmethod
    def is_level_bar(obj, role=None): ...

    @staticmethod
    def is_link(obj, role=None): ...

    @staticmethod
    def is_list(obj, role=None): ...

    @staticmethod
    def is_list_box(obj, role=None): ...

    @staticmethod
    def is_list_item(obj, role=None): ...

    @staticmethod
    def is_log(obj, role=None): ...

    @staticmethod
    def is_mark(obj, role=None): ...

    @staticmethod
    def is_marquee(obj, role=None): ...

    @staticmethod
    def is_math(obj, role=None): ...

    @staticmethod
    def is_math_fraction(obj, role=None): ...

    @staticmethod
    def is_math_root(obj, role=None): ...

    @staticmethod
    def is_menu(obj, role=None): ...

    @staticmethod
    def is_menu_bar(obj, role=None): ...

    @staticmethod
    def is_menu_item(obj, role=None): ...

    @staticmethod
    def is_menu_item_of_any_kind(obj, role=None): ...

    @staticmethod
    def is_menu_related(obj, role=None): ...

    @staticmethod
    def is_modal_dialog(obj, role=None): ...

    @staticmethod
    def is_multi_line_entry(obj, role=None): ...

    @staticmethod
    def is_notification(obj, role=None): ...

    @staticmethod
    def is_option_pane(obj, role=None): ...

    @staticmethod
    def is_page(obj, role=None): ...

    @staticmethod
    def is_page_tab(obj, role=None): ...

    @staticmethod
    def is_page_tab_list(obj, role=None): ...

    @staticmethod
    def is_page_tab_list_related(obj, role=None): ...

    @staticmethod
    def is_panel(obj, role=None): ...

    @staticmethod
    def is_paragraph(obj, role=None): ...

    @staticmethod
    def is_password_text(obj, role=None): ...

    @staticmethod
    def is_popup_menu(obj, role=None): ...

    @staticmethod
    def is_progress_bar(obj, role=None): ...

    @staticmethod
    def is_push_button(obj, role=None): ...

    @staticmethod
    def is_push_button_menu(obj, role=None): ...

    @staticmethod
    def is_radio_button(obj, role=None): ...

    @staticmethod
    def is_radio_menu_item(obj, role=None): ...

    @staticmethod
    def is_rating(obj, role=None): ...

    @staticmethod
    def is_redundant_object(obj, role=None): ...

    @staticmethod
    def is_root_pane(obj, role=None): ...

    @staticmethod
    def is_row_header(obj, role=None): ...

    @staticmethod
    def is_ruler(obj, role=None): ...

    @staticmethod
    def is_scroll_bar(obj, role=None): ...

    @staticmethod
    def is_scroll_pane(obj, role=None): ...

    @staticmethod
    def is_section(obj, role=None): ...

    @staticmethod
    def is_separator(obj, role=None): ...

    @staticmethod
    def is_single_line_entry(obj, role=None): ...

    @staticmethod
    def is_slider(obj, role=None): ...

    @staticmethod
    def is_spin_button(obj, role=None): ...

    @staticmethod
    def is_split_pane(obj, role=None): ...

    @staticmethod
    def is_static(obj, role=None): ...

    @staticmethod
    def is_status_bar(obj, role=None): ...

    @staticmethod
    def is_subscript(obj, role=None): ...

    @staticmethod
    def is_subscript_or_superscript(obj, role=None): ...

    @staticmethod
    def is_suggestion(obj, role=None): ...

    @staticmethod
    def is_superscript(obj, role=None): ...

    @staticmethod
    def is_table(obj, role=None): ...

    @staticmethod
    def is_table_cell(obj, role=None): ...

    @staticmethod
    def is_table_cell_or_header(obj, role=None): ...

    @staticmethod
    def is_table_column_header(obj, role=None): ...

    @staticmethod
    def is_table_header(obj, role=None): ...

    @staticmethod
    def is_table_related(obj, role=None, include_caption=False): ...

    @staticmethod
    def is_table_row(obj, role=None): ...

    @staticmethod
    def is_table_row_header(obj, role=None): ...

    @staticmethod
    def is_tearoff_menu_item(obj, role=None): ...

    @staticmethod
    def is_terminal(obj, role=None): ...

    @staticmethod
    def is_text(obj, role=None): ...

    @staticmethod
    def is_text_input(obj, role=None): ...

    @staticmethod
    def is_timer(obj, role=None): ...

    @staticmethod
    def is_title_bar(obj, role=None): ...

    @staticmethod
    def is_toggle_button(obj, role=None): ...

    @staticmethod
    def is_tool_bar(obj, role=None): ...

    @staticmethod
    def is_tool_tip(obj, role=None): ...

    @staticmethod
    def is_tree(obj, role=None): ...

    @staticmethod
    def is_tree_or_tree_table(obj, role=None): ...

    @staticmethod
    def is_tree_related(obj, role=None): ...

    @staticmethod
    def is_tree_item(obj, role=None): ...

    @staticmethod
    def is_tree_table(obj, role=None): ...

    @staticmethod
    def is_unknown(obj, role=None): ...

    @staticmethod
    def is_unknown_or_redundant(obj, role=None): ...

    @staticmethod
    def is_vertical_scrollbar(obj, role=None): ...

    @staticmethod
    def is_vertical_separator(obj, role=None): ...

    @staticmethod
    def is_vertical_slider(obj, role=None): ...

    @staticmethod
    def is_video(obj, role=None): ...

    @staticmethod
    def is_viewport(obj, role=None): ...

    @staticmethod
    def is_window(obj, role=None): ...

    # From ax_utilities_state.py
    @staticmethod
    def has_no_state(obj): ...

    @staticmethod
    def has_popup(obj): ...

    @staticmethod
    def has_tooltip(obj): ...

    @staticmethod
    def is_active(obj): ...

    @staticmethod
    def is_animated(obj): ...

    @staticmethod
    def is_armed(obj): ...

    @staticmethod
    def is_busy(obj): ...

    @staticmethod
    def is_checkable(obj): ...

    @staticmethod
    def is_checked(obj): ...

    @staticmethod
    def is_collapsed(obj): ...

    @staticmethod
    def is_default(obj): ...

    @staticmethod
    def is_defunct(obj): ...

    @staticmethod
    def is_editable(obj): ...

    @staticmethod
    def is_enabled(obj): ...

    @staticmethod
    def is_expandable(obj): ...

    @staticmethod
    def is_expanded(obj): ...

    @staticmethod
    def is_focusable(obj): ...

    @staticmethod
    def is_focused(obj): ...

    @staticmethod
    def is_horizontal(obj): ...

    @staticmethod
    def is_iconified(obj): ...

    @staticmethod
    def is_indeterminate(obj): ...

    @staticmethod
    def is_invalid_state(obj): ...

    @staticmethod
    def is_invalid_entry(obj): ...

    @staticmethod
    def is_modal(obj): ...

    @staticmethod
    def is_multi_line(obj): ...

    @staticmethod
    def is_multiselectable(obj): ...

    @staticmethod
    def is_opaque(obj): ...

    @staticmethod
    def is_pressed(obj): ...

    @staticmethod
    def is_read_only(obj): ...

    @staticmethod
    def is_required(obj): ...

    @staticmethod
    def is_resizable(obj): ...

    @staticmethod
    def is_selectable(obj): ...

    @staticmethod
    def is_selectable_text(obj): ...

    @staticmethod
    def is_selected(obj): ...

    @staticmethod
    def is_sensitive(obj): ...

    @staticmethod
    def is_showing(obj): ...

    @staticmethod
    def is_single_line(obj): ...

    @staticmethod
    def is_stale(obj): ...

    @staticmethod
    def is_transient(obj): ...

    @staticmethod
    def is_truncated(obj): ...

    @staticmethod
    def is_vertical(obj): ...

    @staticmethod
    def is_visible(obj): ...

    @staticmethod
    def is_visited(obj): ...

    @staticmethod
    def manages_descendants(obj): ...

    @staticmethod
    def supports_autocompletion(obj): ...

    # From ax_utilities_collection.py
    @staticmethod
    def find_all_with_interfaces(root, interface_list, pred=None): ...

    @staticmethod
    def find_all_with_role(root, roles_list, pred=None): ...

    @staticmethod
    def find_all_without_roles(root, role_list, pred=None): ...

    @staticmethod
    def find_all_with_role_and_all_states(root, role_list, state_list, pred=None): ...

    @staticmethod
    def find_all_with_role_and_any_state(root, role_list, state_list, pred=None): ...

    @staticmethod
    def find_all_with_role_without_states(root, role_list, state_list, pred=None): ...

    @staticmethod
    def find_all_with_states(root, state_list, pred=None): ...

    @staticmethod
    def find_all_with_any_state(root, state_list, pred=None): ...

    @staticmethod
    def find_all_without_states(root, state_list, pred=None): ...

    @staticmethod
    def find_all_accelerator_labels(root, pred=None): ...

    @staticmethod
    def find_all_alerts(root, pred=None): ...

    @staticmethod
    def find_all_animations(root, pred=None): ...

    @staticmethod
    def find_all_arrows(root, pred=None): ...

    @staticmethod
    def find_all_articles(root, pred=None): ...

    @staticmethod
    def find_all_audios(root, pred=None): ...

    @staticmethod
    def find_all_autocompletes(root, pred=None): ...

    @staticmethod
    def find_all_block_quotes(root, pred=None): ...

    @staticmethod
    def find_all_buttons(root, pred=None): ...

    @staticmethod
    def find_all_calendars(root, pred=None): ...

    @staticmethod
    def find_all_canvases(root, pred=None): ...

    @staticmethod
    def find_all_captions(root, pred=None): ...

    @staticmethod
    def find_all_charts(root, pred=None): ...

    @staticmethod
    def find_all_check_boxes(root, pred=None): ...

    @staticmethod
    def find_all_check_menu_items(root, pred=None): ...

    @staticmethod
    def find_all_clickables(root, pred=None): ...

    @staticmethod
    def find_all_color_choosers(root, pred=None): ...

    @staticmethod
    def find_all_column_headers(root, pred=None): ...

    @staticmethod
    def find_all_combo_boxes(root, pred=None): ...

    @staticmethod
    def find_all_comments(root, pred=None): ...

    @staticmethod
    def find_all_content_deletions(root, pred=None): ...

    @staticmethod
    def find_all_content_insertions(root, pred=None): ...

    @staticmethod
    def find_all_date_editors(root, pred=None): ...

    @staticmethod
    def find_all_definitions(root, pred=None): ...

    @staticmethod
    def find_all_description_lists(root, pred=None): ...

    @staticmethod
    def find_all_description_terms(root, pred=None): ...

    @staticmethod
    def find_all_description_values(root, pred=None): ...

    @staticmethod
    def find_all_desktop_frames(root, pred=None): ...

    @staticmethod
    def find_all_desktop_icons(root, pred=None): ...

    @staticmethod
    def find_all_dials(root, pred=None): ...

    @staticmethod
    def find_all_dialogs(root, pred=None): ...

    @staticmethod
    def find_all_dialogs_and_alerts(root, pred=None): ...

    @staticmethod
    def find_all_directory_panes(root, pred=None): ...

    @staticmethod
    def find_all_documents(root, pred=None): ...

    @staticmethod
    def find_all_document_emails(root, pred=None): ...

    @staticmethod
    def find_all_document_frames(root, pred=None): ...

    @staticmethod
    def find_all_document_presentations(root, pred=None): ...

    @staticmethod
    def find_all_document_spreadsheets(root, pred=None): ...

    @staticmethod
    def find_all_document_texts(root, pred=None): ...

    @staticmethod
    def find_all_document_webs(root, pred=None): ...

    @staticmethod
    def find_all_drawing_areas(root, pred=None): ...

    @staticmethod
    def find_all_editable_objects(root, pred=None): ...

    @staticmethod
    def find_all_editbars(root, pred=None): ...

    @staticmethod
    def find_all_embeddeds(root, pred=None): ...

    @staticmethod
    def find_all_entries(root, pred=None): ...

    @staticmethod
    def find_all_extendeds(root, pred=None): ...

    @staticmethod
    def find_all_file_choosers(root, pred=None): ...

    @staticmethod
    def find_all_fillers(root, pred=None): ...

    @staticmethod
    def find_all_focus_traversables(root, pred=None): ...

    @staticmethod
    def find_all_focusable_objects(root, pred=None): ...

    @staticmethod
    def find_all_focusable_objects_with_click_ancestor(root, pred=None): ...

    @staticmethod
    def find_all_focused_objects(root, pred=None): ...

    @staticmethod
    def find_all_font_choosers(root, pred=None): ...

    @staticmethod
    def find_all_footers(root, pred=None): ...

    @staticmethod
    def find_all_footnotes(root, pred=None): ...

    @staticmethod
    def find_all_forms(root, pred=None): ...

    @staticmethod
    def find_all_form_fields(root, must_be_focusable=True, pred=None): ...

    @staticmethod
    def find_all_frames(root, pred=None): ...

    @staticmethod
    def find_all_glass_panes(root, pred=None): ...

    @staticmethod
    def find_all_grids(root, pred=None): ...

    @staticmethod
    def find_all_grid_cells(root, pred=None): ...

    @staticmethod
    def find_all_groupings(root, pred=None): ...

    @staticmethod
    def find_all_headers(root, pred=None): ...

    @staticmethod
    def find_all_headings(root, pred=None): ...

    @staticmethod
    def find_all_headings_at_level(root, level, pred=None): ...

    @staticmethod
    def find_all_html_containers(root, pred=None): ...

    @staticmethod
    def find_all_horizontal_scrollbars(root, pred=None): ...

    @staticmethod
    def find_all_horizontal_separators(root, pred=None): ...

    @staticmethod
    def find_all_horizontal_sliders(root, pred=None): ...

    @staticmethod
    def find_all_icons(root, pred=None): ...

    @staticmethod
    def find_all_icons_and_canvases(root, pred=None): ...

    @staticmethod
    def find_all_images(root, pred=None): ...

    @staticmethod
    def find_all_images_and_canvases(root, pred=None): ...

    @staticmethod
    def find_all_images_and_image_maps(root, pred=None): ...

    @staticmethod
    def find_all_image_maps(root, pred=None): ...

    @staticmethod
    def find_all_info_bars(root, pred=None): ...

    @staticmethod
    def find_all_input_method_windows(root, pred=None): ...

    @staticmethod
    def find_all_internal_frames(root, pred=None): ...

    @staticmethod
    def find_all_labels(root, pred=None): ...

    @staticmethod
    def find_all_labels_and_captions(root, pred=None): ...

    @staticmethod
    def find_all_landmarks(root, pred=None): ...

    @staticmethod
    def find_all_layered_panes(root, pred=None): ...

    @staticmethod
    def find_all_level_bars(root, pred=None): ...

    @staticmethod
    def find_all_links(root, must_be_focusable=True, pred=None): ...

    @staticmethod
    def find_all_lists(root, pred=None): ...

    @staticmethod
    def find_all_list_boxes(root, pred=None): ...

    @staticmethod
    def find_all_list_items(root, pred=None): ...

    @staticmethod
    def find_all_live_regions(root, pred=None): ...

    @staticmethod
    def find_all_logs(root, pred=None): ...

    @staticmethod
    def find_all_marks(root, pred=None): ...

    @staticmethod
    def find_all_marquees(root, pred=None): ...

    @staticmethod
    def find_all_maths(root, pred=None): ...

    @staticmethod
    def find_all_math_fractions(root, pred=None): ...

    @staticmethod
    def find_all_math_roots(root, pred=None): ...

    @staticmethod
    def find_all_menus(root, pred=None): ...

    @staticmethod
    def find_all_menu_bars(root, pred=None): ...

    @staticmethod
    def find_all_menu_items(root, pred=None): ...

    @staticmethod
    def find_all_menu_items_of_any_kind(root, pred=None): ...

    @staticmethod
    def find_all_menu_related_objects(root, pred=None): ...

    @staticmethod
    def find_all_modal_dialogs(root, pred=None): ...

    @staticmethod
    def find_all_multi_line_entries(root, pred=None): ...

    @staticmethod
    def find_all_notifications(root, pred=None): ...

    @staticmethod
    def find_all_option_panes(root, pred=None): ...

    @staticmethod
    def find_all_pages(root, pred=None): ...

    @staticmethod
    def find_all_page_tabs(root, pred=None): ...

    @staticmethod
    def find_all_page_tab_lists(root, pred=None): ...

    @staticmethod
    def find_all_page_tab_list_related_objects(root, pred=None): ...

    @staticmethod
    def find_all_panels(root, pred=None): ...

    @staticmethod
    def find_all_paragraphs(root, treat_headings_as_paragraphs=False, pred=None): ...

    @staticmethod
    def find_all_password_texts(root, pred=None): ...

    @staticmethod
    def find_all_popup_menus(root, pred=None): ...

    @staticmethod
    def find_all_progress_bars(root, pred=None): ...

    @staticmethod
    def find_all_push_buttons(root, pred=None): ...

    @staticmethod
    def find_all_push_button_menus(root, pred=None): ...

    @staticmethod
    def find_all_radio_buttons(root, pred=None): ...

    @staticmethod
    def find_all_radio_menu_items(root, pred=None): ...

    @staticmethod
    def find_all_ratings(root, pred=None): ...

    @staticmethod
    def find_all_root_panes(root, pred=None): ...

    @staticmethod
    def find_all_row_headers(root, pred=None): ...

    @staticmethod
    def find_all_rulers(root, pred=None): ...

    @staticmethod
    def find_all_scroll_bars(root, pred=None): ...

    @staticmethod
    def find_all_scroll_panes(root, pred=None): ...

    @staticmethod
    def find_all_sections(root, pred=None): ...

    @staticmethod
    def find_all_selectable_objects(root, pred=None): ...

    @staticmethod
    def find_all_selected_objects(root, pred=None): ...

    @staticmethod
    def find_all_separators(root, pred=None): ...

    @staticmethod
    def find_all_set_containers(root, pred=None): ...

    @staticmethod
    def find_all_showing_objects(root, pred=None): ...

    @staticmethod
    def find_all_showing_and_visible_objects(root, pred=None): ...

    @staticmethod
    def find_all_showing_or_visible_objects(root, pred=None): ...

    @staticmethod
    def find_all_single_line_entries(root, pred=None): ...

    @staticmethod
    def find_all_sliders(root, pred=None): ...

    @staticmethod
    def find_all_spin_buttons(root, pred=None): ...

    @staticmethod
    def find_all_split_panes(root, pred=None): ...

    @staticmethod
    def find_all_statics(root, pred=None): ...

    @staticmethod
    def find_all_status_bars(root, pred=None): ...

    @staticmethod
    def find_all_subscripts(root, pred=None): ...

    @staticmethod
    def find_all_subscripts_and_superscripts(root, pred=None): ...

    @staticmethod
    def find_all_suggestions(root, pred=None): ...

    @staticmethod
    def find_all_superscripts(root, pred=None): ...

    @staticmethod
    def find_all_supports_action(root, pred=None): ...

    @staticmethod
    def find_all_supports_document(root, pred=None): ...

    @staticmethod
    def find_all_supports_editable_text(root, pred=None): ...

    @staticmethod
    def find_all_supports_hypertext(root, pred=None): ...

    @staticmethod
    def find_all_supports_hyperlink(root, pred=None): ...

    @staticmethod
    def find_all_supports_selection(root, pred=None): ...

    @staticmethod
    def find_all_supports_table(root, pred=None): ...

    @staticmethod
    def find_all_supports_table_cell(root, pred=None): ...

    @staticmethod
    def find_all_supports_text(root, pred=None): ...

    @staticmethod
    def find_all_supports_value(root, pred=None): ...

    @staticmethod
    def find_all_tables(root, pred=None): ...

    @staticmethod
    def find_all_table_cells(root, pred=None): ...

    @staticmethod
    def find_all_table_cells_and_headers(root, pred=None): ...

    @staticmethod
    def find_all_table_column_headers(root, pred=None): ...

    @staticmethod
    def find_all_table_headers(root, pred=None): ...

    @staticmethod
    def find_all_table_related_objects(root, pred=None, include_caption=False): ...

    @staticmethod
    def find_all_table_rows(root, pred=None): ...

    @staticmethod
    def find_all_table_row_headers(root, pred=None): ...

    @staticmethod
    def find_all_tearoff_menu_items(root, pred=None): ...

    @staticmethod
    def find_all_terminals(root, pred=None): ...

    @staticmethod
    def find_all_texts(root, pred=None): ...

    @staticmethod
    def find_all_text_inputs(root, pred=None): ...

    @staticmethod
    def find_all_timers(root, pred=None): ...

    @staticmethod
    def find_all_title_bars(root, pred=None): ...

    @staticmethod
    def find_all_toggle_buttons(root, pred=None): ...

    @staticmethod
    def find_all_tool_bars(root, pred=None): ...

    @staticmethod
    def find_all_tool_tips(root, pred=None): ...

    @staticmethod
    def find_all_trees(root, pred=None): ...

    @staticmethod
    def find_all_trees_and_tree_tables(root, pred=None): ...

    @staticmethod
    def find_all_tree_related_objects(root, pred=None): ...

    @staticmethod
    def find_all_tree_items(root, pred=None): ...

    @staticmethod
    def find_all_tree_tables(root, pred=None): ...

    @staticmethod
    def find_all_unrelated_labels(root, must_be_showing=True, pred=None): ...

    @staticmethod
    def find_all_unvisited_links(root, must_be_focusable=True, pred=None): ...

    @staticmethod
    def find_all_vertical_scrollbars(root, pred=None): ...

    @staticmethod
    def find_all_vertical_separators(root, pred=None): ...

    @staticmethod
    def find_all_vertical_sliders(root, pred=None): ...

    @staticmethod
    def find_all_videos(root, pred=None): ...

    @staticmethod
    def find_all_viewports(root, pred=None): ...

    @staticmethod
    def find_all_visible_objects(root, pred=None): ...

    @staticmethod
    def find_all_visited_links(root, must_be_focusable=True, pred=None): ...

    @staticmethod
    def find_default_button(root): ...

    @staticmethod
    def find_focused_object(root): ...

    @staticmethod
    def find_status_bar(root): ...

    @staticmethod
    def has_combo_box_or_list_box(root): ...

    @staticmethod
    def has_editable_object(root): ...

    @staticmethod
    def has_scroll_pane(root): ...

    @staticmethod
    def has_split_pane(root): ...

    @staticmethod
    def has_tree_or_tree_table(root): ...
