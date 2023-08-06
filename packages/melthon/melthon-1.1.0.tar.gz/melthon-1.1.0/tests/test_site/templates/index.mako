<%inherit file="base.template.mako"/>

<%block name="content">
    <h1>Fruits</h1>
    % for (color, fruits) in data['fruits'].items():
        <p>${color}</p>
        <ul>
            % for fruit in fruits:
                <li>${fruit}</li>
            % endfor
        </ul>
    % endfor

    <h1>Vegetables</h1>
    <ul>
        % for vegetable in vegetables:
            <li>${vegetable}</li>
        % endfor
    </ul>
</%block>
