## -*- coding: utf-8; -*-
<%inherit file="/master/view.mako" />

<%def name="extra_styles()">
  ${parent.extra_styles()}
  % if use_buefy:
      <style type="text/css">
        #main-product-panel {
            margin-right: 2em;
            margin-top: 1em;
        }
        #pricing-panel .field-wrapper .field {
            white-space: nowrap;
        }
      </style>
  % endif
</%def>

<%def name="render_main_fields(form)">
  ${form.render_field_readonly('upc')}
  ${form.render_field_readonly('brand')}
  ${form.render_field_readonly('description')}
  ${form.render_field_readonly('size')}
  ${form.render_field_readonly('unit_size')}
  ${form.render_field_readonly('unit_of_measure')}
  ${form.render_field_readonly('case_size')}
  % if instance.is_pack_item():
      ${form.render_field_readonly('pack_size')}
      ${form.render_field_readonly('unit')}
      ${form.render_field_readonly('default_pack')}
  % elif instance.packs:
      ${form.render_field_readonly('packs')}
  % endif
  ${self.extra_main_fields(form)}
</%def>

<%def name="left_column()">
  % if use_buefy:
      <nav class="panel" id="pricing-panel">
        <p class="panel-heading">Pricing</p>
        <div class="panel-block">
          <div>
            ${self.render_price_fields(form)}
          </div>
        </div>
      </nav>
      <nav class="panel">
        <p class="panel-heading">Flags</p>
        <div class="panel-block">
          <div>
            ${self.render_flag_fields(form)}
          </div>
        </div>
      </nav>
  % else:
  <div class="panel">
    <h2>Pricing</h2>
    <div class="panel-body">
      ${self.render_price_fields(form)}
    </div>
  </div>
  <div class="panel">
    <h2>Flags</h2>
    <div class="panel-body">
      ${self.render_flag_fields(form)}
    </div>
  </div>
  % endif
  ${self.extra_left_panels()}
</%def>

<%def name="right_column()">
  ${self.organization_panel()}
  ${self.movement_panel()}
  ${self.sources_panel()}
  ${self.notes_panel()}
  ${self.ingredients_panel()}
  ${self.lookup_codes_panel()}
  ${self.extra_right_panels()}
</%def>

<%def name="extra_main_fields(form)"></%def>

<%def name="organization_panel()">
  % if use_buefy:
      <nav class="panel">
        <p class="panel-heading">Organization</p>
        <div class="panel-block">
          <div>
            ${self.render_organization_fields(form)}
          </div>
        </div>
      </nav>
  % else:
  <div class="panel">
    <h2>Organization</h2>
    <div class="panel-body">
      ${self.render_organization_fields(form)}
    </div>
  </div>
  % endif
</%def>

<%def name="render_organization_fields(form)">
    ${form.render_field_readonly('department')}
    ${form.render_field_readonly('subdepartment')}
    ${form.render_field_readonly('category')}
    ${form.render_field_readonly('family')}
    ${form.render_field_readonly('report_code')}
</%def>

<%def name="render_price_fields(form)">
    ${form.render_field_readonly('price_required')}
    ${form.render_field_readonly('regular_price')}
    ${form.render_field_readonly('current_price')}
    ${form.render_field_readonly('current_price_ends')}
    ${form.render_field_readonly('suggested_price')}
    ${form.render_field_readonly('deposit_link')}
    ${form.render_field_readonly('tax')}
</%def>

<%def name="render_flag_fields(form)">
    ${form.render_field_readonly('weighed')}
    ${form.render_field_readonly('discountable')}
    ${form.render_field_readonly('special_order')}
    ${form.render_field_readonly('organic')}
    ${form.render_field_readonly('not_for_sale')}
    ${form.render_field_readonly('discontinued')}
    ${form.render_field_readonly('deleted')}
</%def>

<%def name="movement_panel()">
  % if use_buefy:
      <nav class="panel">
        <p class="panel-heading">Movement</p>
        <div class="panel-block">
          <div>
            ${self.render_movement_fields(form)}
          </div>
        </div>
      </nav>
  % else:
  <div class="panel">
    <h2>Movement</h2>
    <div class="panel-body">
      ${self.render_movement_fields(form)}
    </div>
  </div>
  % endif
</%def>

<%def name="render_movement_fields(form)">
    ${form.render_field_readonly('last_sold')}
</%def>

<%def name="lookup_codes_grid()">
  <div class="grid full no-border">
    <table>
      <thead>
        <th>Seq</th>
        <th>Code</th>
      </thead>
      <tbody>
        % for code in instance._codes:
            <tr>
              <td>${code.ordinal}</td>
              <td>${code.code}</td>
            </tr>
        % endfor
      </tbody>
    </table>
  </div>
</%def>

<%def name="lookup_codes_panel()">
  % if use_buefy:
      <nav class="panel">
        <p class="panel-heading">Additional Lookup Codes</p>
        <div class="panel-block">
          ${self.lookup_codes_grid()}
        </div>
      </nav>
  % else:
  <div class="panel-grid" id="product-codes">
    <h2>Additional Lookup Codes</h2>
    ${self.lookup_codes_grid()}
  </div>
  % endif
</%def>

<%def name="sources_grid()">
  <div class="grid full no-border">
    <table>
      <thead>
        <th>${costs_label_preferred}</th>
        <th>${costs_label_vendor}</th>
        <th>${costs_label_code}</th>
        <th>${costs_label_case_size}</th>
        <th>Case Cost</th>
        <th>Unit Cost</th>
        <th>Status</th>
      </thead>
      <tbody>
        % for i, cost in enumerate(instance.costs, 1):
            <tr class="${'even' if i % 2 == 0 else 'odd'}">
              <td class="center">${'X' if cost.preference == 1 else ''}</td>
              <td>
                % if request.has_perm('vendors.view'):
                    ${h.link_to(cost.vendor, request.route_url('vendors.view', uuid=cost.vendor_uuid))}
                % else:
                    ${cost.vendor}
                % endif
              </td>
              <td class="center">${cost.code or ''}</td>
              <td class="center">${h.pretty_quantity(cost.case_size)}</td>
              <td class="right">${'$ %0.2f' % cost.case_cost if cost.case_cost is not None else ''}</td>
              <td class="right">${'$ %0.4f' % cost.unit_cost if cost.unit_cost is not None else ''}</td>
              <td>${"discontinued" if cost.discontinued else "available"}</td>
            </tr>
        % endfor
      </tbody>
    </table>
  </div>
</%def>

<%def name="sources_panel()">
  % if use_buefy:
      <nav class="panel">
        <p class="panel-heading">Vendor Sources</p>
        <div class="panel-block">
          ${self.sources_grid()}
        </div>
      </nav>
  % else:
  <div class="panel-grid" id="product-costs">
    <h2>Vendor Sources</h2>
    ${self.sources_grid()}
  </div>
  % endif
</%def>

<%def name="notes_panel()">
  % if use_buefy:
      <nav class="panel">
        <p class="panel-heading">Notes</p>
        <div class="panel-block">
          <div class="field">${form.render_field_readonly('notes')}</div>
        </div>
      </nav>
  % else:
  <div class="panel">
    <h2>Notes</h2>
    <div class="panel-body">
      <div class="field">${form.render_field_readonly('notes')}</div>
    </div>
  </div>
  % endif
</%def>

<%def name="ingredients_panel()">
  % if use_buefy:
      <nav class="panel">
        <p class="panel-heading">Ingredients</p>
        <div class="panel-block">
          ${form.render_field_readonly('ingredients')}
        </div>
      </nav>
  % else:
  <div class="panel">
    <h2>Ingredients</h2>
    <div class="panel-body">
      ${form.render_field_readonly('ingredients')}
    </div>
  </div>
  % endif
</%def>

<%def name="extra_left_panels()"></%def>

<%def name="extra_right_panels()"></%def>

<%def name="page_content()">
  % if use_buefy:
          <div style="display: flex; flex-direction: column;">

            <nav class="panel" id="main-product-panel">
              <p class="panel-heading">Product</p>
              <div class="panel-block">
                <div style="display: flex; justify-content: space-between; width: 100%;">
                  <div>
                    ${self.render_main_fields(form)}
                  </div>
                  <div>
                    % if image_url:
                        ${h.image(image_url, "Product Image", id='product-image', width=150, height=150)}
                    % endif
                  </div>
                </div>
              </div>
            </nav>

            <div style="display: flex;">
              <div class="panel-wrapper"> <!-- left column -->
                ${self.left_column()}
              </div> <!-- left column -->
              <div class="panel-wrapper" style="margin-left: 1em;"> <!-- right column -->
                ${self.right_column()}
              </div> <!-- right column -->
            </div>

          </div>

  % else:
      ## legacy / not buefy

        <div style="display: flex; flex-direction: column;">

          <div class="panel" id="product-main">
            <h2>Product</h2>
            <div class="panel-body">
              <div style="display: flex; justify-content: space-between;">
                <div>
                  ${self.render_main_fields(form)}
                </div>
                <div>
                  % if image_url:
                      ${h.image(image_url, "Product Image", id='product-image', width=150, height=150)}
                  % endif
                </div>
              </div>
            </div>
          </div>

          <div style="display: flex;">
            <div class="panel-wrapper"> <!-- left column -->
              ${self.left_column()}
            </div> <!-- left column -->
            <div class="panel-wrapper" style="margin-left: 1em;"> <!-- right column -->
              ${self.right_column()}
            </div> <!-- right column -->
          </div>

        </div>
  % endif

  % if buttons:
      ${buttons|n}
  % endif
</%def>


${parent.body()}
