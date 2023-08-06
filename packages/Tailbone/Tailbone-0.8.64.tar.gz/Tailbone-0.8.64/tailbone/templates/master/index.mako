## -*- coding: utf-8; -*-
## ##############################################################################
## 
## Default master 'index' template.  Features a prominent data table and
## exposes a way to filter and sort the data, etc.  Some index pages also
## include a "tools" section, just above the grid on the right.
## 
## ##############################################################################
<%inherit file="/page.mako" />

<%def name="title()">${index_title}</%def>

<%def name="content_title()"></%def>

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  % if not use_buefy:
  <script type="text/javascript">
    $(function() {

        $('.grid-wrapper').gridwrapper();

        % if master.deletable and request.has_perm('{}.delete'.format(permission_prefix)) and master.delete_confirm == 'simple':

            $('.grid-wrapper').on('click', '.grid .actions a.delete', function() {
                if (confirm("Are you sure you wish to delete this ${model_title}?")) {
                    var link = $(this).get(0);
                    var form = $('#delete-object-form').get(0);
                    form.action = link.href;
                    form.submit();
                }
                return false;
            });

        % endif

        % if master.mergeable and request.has_perm('{}.merge'.format(permission_prefix)):

            $('form[name="merge-things"] button').button('option', 'disabled', $('.grid').gridcore('count_selected') != 2);

            $('.grid-wrapper').on('gridchecked', '.grid', function(event, count) {
                $('form[name="merge-things"] button').button('option', 'disabled', count != 2);
            });

            $('form[name="merge-things"]').submit(function() {
                var uuids = $('.grid').gridcore('selected_uuids');
                if (uuids.length != 2) {
                    return false;
                }
                $(this).find('[name="uuids"]').val(uuids.toString());
                $(this).find('button')
                    .button('option', 'label', "Preparing to Merge...")
                    .button('disable');
            });

        % endif

        % if master.bulk_deletable and request.has_perm('{}.bulk_delete'.format(permission_prefix)):

        $('form[name="bulk-delete"] button').click(function() {
            var count = $('.grid-wrapper').gridwrapper('results_count', true);
            if (count === null) {
                alert("There don't seem to be any results to delete!");
                return;
            }
            if (! confirm("You are about to delete " + count + " ${model_title_plural}.\n\nAre you sure?")) {
                return
            }
            $(this).button('disable').button('option', 'label', "Deleting Results...");
            $('form[name="bulk-delete"]').submit();
        });

        % endif

        % if master.supports_set_enabled_toggle and request.has_perm('{}.enable_disable_set'.format(permission_prefix)):
            $('form[name="enable-set"] button').click(function() {
                var form = $(this).parents('form');
                var uuids = $('.grid').gridcore('selected_uuids');
                if (! uuids.length) {
                    alert("You must first select one or more objects to enable.");
                    return false;
                }
                if (! confirm("Are you sure you wish to ENABLE the " + uuids.length + " selected objects?")) {
                    return false;
                }
                form.find('[name="uuids"]').val(uuids.toString());
                disable_button(this);
                form.submit();
            });

            $('form[name="disable-set"] button').click(function() {
                var form = $(this).parents('form');
                var uuids = $('.grid').gridcore('selected_uuids');
                if (! uuids.length) {
                    alert("You must first select one or more objects to disable.");
                    return false;
                }
                if (! confirm("Are you sure you wish to DISABLE the " + uuids.length + " selected objects?")) {
                    return false;
                }
                form.find('[name="uuids"]').val(uuids.toString());
                disable_button(this);
                form.submit();
            });
        % endif

        % if master.set_deletable and request.has_perm('{}.delete_set'.format(permission_prefix)):
            $('form[name="delete-set"] button').click(function() {
                var form = $(this).parents('form');
                var uuids = $('.grid').gridcore('selected_uuids');
                if (! uuids.length) {
                    alert("You must first select one or more objects to delete.");
                    return false;
                }
                if (! confirm("Are you sure you wish to DELETE the " + uuids.length + " selected objects?")) {
                    return false;
                }
                form.find('[name="uuids"]').val(uuids.toString());
                disable_button(this);
                form.submit();
            });
        % endif
    });
  </script>
  % endif
</%def>

<%def name="context_menu_items()">
  % if master.results_downloadable_csv and request.has_perm('{}.results_csv'.format(permission_prefix)):
      <li>${h.link_to("Download results as CSV", url('{}.results_csv'.format(route_prefix)))}</li>
  % endif
  % if master.results_downloadable_xlsx and request.has_perm('{}.results_xlsx'.format(permission_prefix)):
      <li>${h.link_to("Download results as XLSX", url('{}.results_xlsx'.format(route_prefix)))}</li>
  % endif
  % if master.creatable and master.show_create_link and request.has_perm('{}.create'.format(permission_prefix)):
      % if master.creates_multiple:
          <li>${h.link_to("Create new {}".format(model_title_plural), url('{}.create'.format(route_prefix)))}</li>
      % else:
          <li>${h.link_to("Create a new {}".format(model_title), url('{}.create'.format(route_prefix)))}</li>
      % endif
  % endif
</%def>

<%def name="grid_tools()">

  ## merge 2 objects
  % if master.mergeable and request.has_perm('{}.merge'.format(permission_prefix)):

      % if use_buefy:
      ${h.form(url('{}.merge'.format(route_prefix)), **{'@submit': 'submitMergeForm'})}
      % else:
      ${h.form(url('{}.merge'.format(route_prefix)), name='merge-things')}
      % endif
      ${h.csrf_token(request)}
      % if use_buefy:
          <input type="hidden"
                 name="uuids"
                 :value="checkedRowUUIDs()" />
          <b-button type="is-primary"
                    native-type="submit"
                    icon-pack="fas"
                    icon-left="object-ungroup"
                    :disabled="mergeFormSubmitting || checkedRows.length != 2">
            {{ mergeFormButtonText }}
          </b-button>
      % else:
          ${h.hidden('uuids')}
          <button type="submit" class="button">Merge 2 ${model_title_plural}</button>
      % endif
      ${h.end_form()}
  % endif

  ## enable / disable selected objects
  % if master.supports_set_enabled_toggle and request.has_perm('{}.enable_disable_set'.format(permission_prefix)):
      ${h.form(url('{}.enable_set'.format(route_prefix)), name='enable-set', class_='control')}
      ${h.csrf_token(request)}
      ${h.hidden('uuids')}
      <button type="button" class="button">Enable Selected</button>
      ${h.end_form()}

      ${h.form(url('{}.disable_set'.format(route_prefix)), name='disable-set', class_='control')}
      ${h.csrf_token(request)}
      ${h.hidden('uuids')}
      <button type="button" class="button">Disable Selected</button>
      ${h.end_form()}
  % endif

  ## delete selected objects
  % if master.set_deletable and request.has_perm('{}.delete_set'.format(permission_prefix)):
      ${h.form(url('{}.delete_set'.format(route_prefix)), name='delete-set', class_='control')}
      ${h.csrf_token(request)}
      ${h.hidden('uuids')}
      <button type="button" class="button">Delete Selected</button>
      ${h.end_form()}
  % endif

  ## delete search results
  % if master.bulk_deletable and request.has_perm('{}.bulk_delete'.format(permission_prefix)):
      ${h.form(url('{}.bulk_delete'.format(route_prefix)), name='bulk-delete', class_='control')}
      ${h.csrf_token(request)}
      % if use_buefy:
          <b-button type="is-danger"
                    :disabled="! total"
                    :title="total ? null : 'There are no results to delete'"
                    @click="deleteResults"
                    icon-pack="fas"
                    icon-left="trash">
            Delete Results
          </b-button>
      % else:
          <button type="button">Delete Results</button>
      % endif
      ${h.end_form()}
  % endif

</%def>

<%def name="page_content()">
  <tailbone-grid
     % if master.deletable and request.has_perm('{}.delete'.format(permission_prefix)) and master.delete_confirm == 'simple':
     @deleteActionClicked="deleteObject"
     % endif
     >
  </tailbone-grid>
  % if master.deletable and request.has_perm('{}.delete'.format(permission_prefix)) and master.delete_confirm == 'simple':
      ${h.form('#', ref='deleteObjectForm')}
      ${h.csrf_token(request)}
      ${h.end_form()}
  % endif
</%def>

<%def name="modify_this_page_vars()">
  ${parent.modify_this_page_vars()}
  <script type="text/javascript">
    % if master.mergeable and request.has_perm('{}.merge'.format(permission_prefix)):
        TailboneGridData.mergeFormButtonText = "Merge 2 ${model_title_plural}"
        TailboneGridData.mergeFormSubmitting = false
        TailboneGrid.methods.submitMergeForm = function() {
            this.mergeFormSubmitting = true
            this.mergeFormButtonText = "Working, please wait..."
        }
    % endif
    % if master.deletable and request.has_perm('{}.delete'.format(permission_prefix)) and master.delete_confirm == 'simple':
        ThisPage.methods.deleteObject = function(url) {
            if (confirm("Are you sure you wish to delete this ${model_title}?")) {
                let form = this.$refs.deleteObjectForm
                form.action = url
                form.submit()
            }
        }
    % endif
  </script>
</%def>

<%def name="make_this_page_component()">
  ${parent.make_this_page_component()}
  <script type="text/javascript">

    TailboneGrid.data = function() { return TailboneGridData }

    Vue.component('tailbone-grid', TailboneGrid)

  </script>
</%def>

<%def name="render_this_page()">
  ${self.page_content()}
</%def>

<%def name="render_this_page_template()">
  ${parent.render_this_page_template()}

  ## TODO: stop using |n filter
  ${grid.render_buefy(tools=capture(self.grid_tools).strip(), context_menu=capture(self.context_menu_items).strip())|n}
</%def>


% if use_buefy:
    ${parent.body()}

% else:
    ## no buefy, so do the traditional thing
    ${grid.render_complete(tools=capture(self.grid_tools).strip(), context_menu=capture(self.context_menu_items).strip())|n}

    % if master.deletable and request.has_perm('{}.delete'.format(permission_prefix)) and master.delete_confirm == 'simple':
        ${h.form('#', id='delete-object-form')}
        ${h.csrf_token(request)}
        ${h.end_form()}
    % endif
% endif
