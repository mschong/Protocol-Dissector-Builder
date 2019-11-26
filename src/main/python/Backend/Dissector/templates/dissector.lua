protocol = Proto("{{dis.name}}",  "{{dis.description}}")

{% for field in dis.fields %}
    {{field.name}} = ProtoField.{{field.type}}("{{field.des}}","{{dis.name}}"."{{field.abbrev}}",base.{{field.display_type}})
{% endfor %}

protocol.fields = { {% for field in dis.fields %} {{field.name}} {{ "," if not loop.last }} {% endfor%} }

function protocol.dissector(buffer, pinfo, tree)
  pktlen = buffer:reported_length_remaining()

  if length == 0 then return end

  pinfo.cols.protocol = protocol.name

  local subtree = tree:add(protocol, buffer(), "{{dis.subtree_name}}")
  
    {% set offset = namespace(off=0) %}
    {% for field in dis.fields %}
        subtree:add({{field.name}},buffer({{offset.off}},{{field.size}}))
        {% set offset.off = offset.off + field.size %}       
    {% endfor %}

    {% for decision in dis.decisions %}
        if {{{decision.operand1}} {{decision.operator1}} {{decision.operand2}} then


  
end

local port = DissectorTable.get("{{dis.port_type}}.port")
port:add({{dis.port_number}}, protocol)