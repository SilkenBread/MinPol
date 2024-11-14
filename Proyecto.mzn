% Datos de entrada
int: n; % Numero de personas
int: m; % Numero de opiniones
array[1..m] of int: p; % Distribución inicial de personas en cada opinión
array[1..m] of float: v; % Valor real correspondiente a cada opinión
array[1..m] of float: ce; % Costo extra por mover a posición inicialmente vacía
array[1..m, 1..m] of float: C; % Costo base de mover una persona de i a j
float: ct; % Costo total máximo permitido
int: MaxMovs; % Máximo número de movimientos permitidos

% Variables
array[1..m, 1..m] of var 0..n: x; % Número de personas movidas de i a j
array[1..m] of var 0..n: distribucion_final; % Distribución final de personas

% Variables auxiliares para el cálculo de la mediana
array[1..m] of var 0..n: acumulado; % Suma acumulada de personas
var 0..n*m: total_personas_movidas; % Variables para contar movimientos
var 0..MaxMovs: total_pasos_movimientos; % Variables para contar movimientos

% Restricciones

% 1. Calcular la distribución final de personas en cada opinión
constraint forall(i in 1..m) (
    distribucion_final[i] = p[i] + 
                           sum(k in 1..m) (x[k,i]) -  % Personas que llegan a i
                           sum(k in 1..m) (x[i,k])    % Personas que salen de i
);

% 2. No se pueden mover más personas de las que hay en cada opinión inicial
constraint forall(i in 1..m) (
    sum(j in 1..m) (x[i,j]) <= p[i]
);

% 3. Límite de movimientos totales
constraint sum(i in 1..m, j in 1..m) (abs(j - i) * x[i,j]) <= MaxMovs;

% 4. Conservación del número total de personas
constraint sum(i in 1..m) (distribucion_final[i]) = sum(i in 1..m) (p[i]);

% 5. Todas las distribuciones finales deben ser no negativas
constraint forall(i in 1..m) (
    distribucion_final[i] >= 0
);

% 6. Cálculo del acumulado para la mediana
constraint acumulado[1] = distribucion_final[1];
constraint forall(i in 2..m) (
    acumulado[i] = acumulado[i-1] + distribucion_final[i]
);

% 7. Restricción de costo total
var float: costo_total = sum(i in 1..m, j in 1..m) (
    if p[j] > 0 then
        C[i,j] * (1 + p[i] / n) * x[i,j]
    else
        C[i,j] * (1 + p[i] / n) * x[i,j] + ce[j] * x[i,j]
    endif
);
constraint costo_total <= ct;

% 8. Cálculo del total de movimientos
constraint total_personas_movidas = sum(i in 1..m, j in 1..m) (x[i,j]);
constraint total_pasos_movimientos = sum(i in 1..m, j in 1..m) (abs(j - i) * x[i,j]);

% Cálculo de la mediana
var float: valor_mediana1 = sum(i in 1..m) (
    if i = 1 then
        if acumulado[i] >= (n div 2 + 1) then v[i] else 0.0 endif
    else
        if acumulado[i-1] < (n div 2 + 1) /\ acumulado[i] >= (n div 2 + 1) then v[i] else 0.0 endif
    endif
);

var float: valor_mediana2 = sum(i in 1..m) (
    if i = 1 then
        if acumulado[i] >= (n div 2) then v[i] else 0.0 endif
    else
        if acumulado[i-1] < (n div 2) /\ acumulado[i] >= (n div 2) then v[i] else 0.0 endif
    endif
);

var float: mediana = if n mod 2 = 1 then valor_mediana1 else (valor_mediana1 + valor_mediana2) / 2.0 endif;
    
% Función objetivo
var float: polarizacion = sum(j in 1..m) (
    distribucion_final[j] * abs(v[j] - mediana)
);

solve minimize polarizacion;

% Salida
output [
    "Matriz de movimientos:\n",
    show2d(x), "\n",
    "Distribución Inicial: ", show(p), "\n",
    "Distribución Final: ", show(distribucion_final), "\n",
    "Acumulado: ", show(acumulado), "\n",
    "Mediana: ", show_float(2, 2, mediana), "\n",

    "Total de personas movidas: ", show(total_personas_movidas), "\n",
    "Total de pasos realizados: ", show(total_pasos_movimientos), "\n",
    "Polarización: ", show_float(3, 3, polarizacion), "\n",
    "Costo Total: ", show_float(2, 2, costo_total), "\n"
];