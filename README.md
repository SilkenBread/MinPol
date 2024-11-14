# El Problema de Minimizar la Polarización presente en una Población (MinPol)
## Análsis y Diseño de Algoritmos II

#### Introducción
El problema de minimizar la polarización en una población consiste en identificar y ejecutar esfuerzos específicos para modificar la opinión de ciertos grupos de personas, de tal forma que se logre una disminución significativa de la polarización general en la red. En este contexto, cada esfuerzo implica un costo y debe ser asignado de manera estratégica debido a los recursos limitados disponibles. El objetivo es llevar a la población a un estado de opinión más uniforme y menos polarizado. Para abordar esta problemática, se ha formulado un modelo de optimización en MiniZinc, empleando técnicas avanzadas de programación lineal, programación entera y programación entera mixta, así como el método branch and bound, el cual es efectivo para resolver problemas de programación binaria, entera y mixta. Estas técnicas permiten modelar el problema mediante parámetros, variables, restricciones y una función objetivo específica, adaptando el modelo a los recursos disponibles y al objetivo de minimizar la polarización.

#### Ejecución

Instalamos las dependencias del proyecto
```bash
  pip install -r requirements.txt
```

Ejecutamos nuestro programa
```bash
  python main.py
```

## Authors

- Franklin Aguirre
- Manuel Cardoso
- Sebastian Orrego
- Juan David Rodriguez