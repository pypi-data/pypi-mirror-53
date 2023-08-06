## -*- coding: utf-8; -*-
## ##############################################################################
## 
## Default master 'versions' template, for showing an object's version history.
## 
## ##############################################################################
<%inherit file="/page.mako" />

## TODO: this page still uses old-style grid but should use Buefy grid

<%def name="title()">${model_title_plural} » ${instance_title} » history</%def>

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  <script type="text/javascript">
    $(function() {
        $('.grid-wrapper').gridwrapper();
    });
  </script>
</%def>

<%def name="content_title()">
  History for ${instance_title}
</%def>

<%def name="page_content()">
  ${grid.render_complete()|n}
</%def>


${parent.body()}
