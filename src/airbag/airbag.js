
Handlebars.registerHelper('source_table', function(frame, options) {
  var output = [];
  for(var i=0; i < frame.source_context.length; i++) {
    var lineno = i + frame.start_lineno;
    var className =  (lineno == frame.lineno) ? "traceline" : "normal";

    output.push("<tr class='" + className + "'><td class='lineno'>");
    output.push(lineno + 1 + ".  </td><td><pre>" + frame.source_context[i] +"</pre></td></tr>");
  }

  return output.join("");
});

Handlebars.registerHelper('variables_table', function(variables, options) {
  var output = [];
  for (var name in variables) {
    var value = variables[name];
    output.push("<tr><td>" +  name + "</td><td>=</td><td>" +  value + "</td></tr>");
  }

  return output.join("");
});

var template = Handlebars.compile($("#crash-template").html());
$('body').append(template(data));
