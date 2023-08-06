## -*- coding: utf-8; -*-
<%inherit file="/page.mako" />

<%def name="title()">Change Password</%def>

<%def name="page_content()">
  <div class="form">
    ${form.render_deform()|n}
  </div>
</%def>


${parent.body()}
