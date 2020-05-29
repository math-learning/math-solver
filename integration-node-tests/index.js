const fs = require('fs');
const path = require('path');
const fetch = require('node-fetch');

const mathSolverBasePath = 'http://localhost:5000';

const functions = {
  x: {
    'func': 'a1*x^{b1}',
    'deriv': 'a1*b1*x^{b1-1}'
  },
  cosx: {
    'func': 'a1*\\cos(x)',
    'deriv': '-a1*\\sin{\\left(x \\right)}'
  },
  senx: {
    'func': 'a1*\\sin(x)',
    'deriv': 'a1*\\cos{\\left(x \\right)}'
  },
  tagx: {
    'func': 'a1*\\tan(x)',
    'deriv': 'a1*\\frac{1}{{\\cos(x)}^2}'
  },
  sqrt: {
    'func': 'a1*\\sqrt[b1]{x}',
    'deriv': 'a1*\\frac{1}{b1} * x^{\\frac{1}{b1}-1}'
  },
  '1/x': {
    'func': 'a1*\\frac{1}{x}',
    'deriv': '-a1*\\frac{1}{x^{2}}'
  }
  // expx: {
  //   'func': 'a1*\\exp(x)',
  //   'deriv': 'a1*\\exp(x)'
  // }
}

const possible_theorems = {
  'f+g': {
    text: 'f+g',
    input: '\\frac{d(f1+g1)}{dx}',
    type: 'derivative',
    steps: [
      { expression: '\\frac{d(f1+g1)}{dx}', status: 'valid' },
      { expression: '\\frac{d(f1)}{dx} + \\frac{d(g1)}{dx}', status: 'valid' },
      { expression: '\\frac{d(f1)}{dx} + dg1', status: 'valid' },
      { expression: 'dg1 + \\frac{d(f1)}{dx}', status: 'valid' },
      { expression: 'df1 + dg1', status: 'resolved' },
      { expression: 'dg1 + df1', status: 'resolved' },

      { expression: 'df1 - dg1', status: 'invalid' },
      { expression: '\\frac{d(f1)}{dx} + 2*dg1', status: 'invalid' },
      { expression: 'dg1', status: 'invalid' },
      { expression: 'df1', status: 'invalid' },
    ]
  },
  'f-g': {
    text: 'f1-g1',
    input: '\\frac{d(f1-g1)}{dx}',
    type: 'derivative',
    steps: [
      { expression: '\\frac{d(f1-g1)}{dx}', status: 'valid' },
      { expression: '\\frac{d(f1)}{dx} - dg1', status: 'valid' },
      { expression: '-dg1 + \\frac{d(f1)}{dx}', status: 'valid' },
      { expression: 'df1 - dg1', status: 'resolved' },
      { expression: '-dg1 + df1', status: 'resolved' },

      { expression: 'df1 + dg1', status: 'invalid' },
      { expression: '\\frac{d(f1)}{dx} - 2*dg1', status: 'invalid' },
      { expression: 'dg1', status: 'invalid' },
      { expression: 'df1', status: 'invalid' },
    ]
  },
  'f*g': {
    text: 'f*g',
    input: '\\frac{d(f1*g1)}{dx}',
    type: 'derivative',
    steps: [
      { expression: '\\frac{d(f1*g1)}{dx}', status: 'valid' },
      { expression: '\\frac{d(f1)}{dx}*g1 + f1*\\frac{d(g1)}{dx}', status: 'valid' },
      { expression: 'df1*g1 + f1*\\frac{d(g1)}{dx}', status: 'valid' },
      { expression: '\\frac{d(f1)}{dx}*g1 + f1*dg1', status: 'valid' },
      { expression: 'df1*g1 + f1*dg1', status: 'resolved' },
      { expression: 'f1*dg1 + df1*g1', status: 'resolved' },

      { expression: 'df1*g1 - f1*\\frac{d(g1)}{dx}', status: 'invalid' },
      { expression: 'df1*g1', status: 'invalid' },
      { expression: 'f1*dg1', status: 'invalid' },   
    ]
  },
  'f/g': {
    text: 'f1/g1',
    input: '\\frac{d(\\frac{f1}{g1})}{dx}',
    type: 'derivative',
    steps: [
      { expression: '\\frac{d(\\frac{f1}{g1})}{dx}', status: 'valid' },
      { expression: '\\frac{\\frac{d(f1)}{dx}*g1 - f1*\\frac{d(g1)}{dx}}{{g1}^{2}}', status: 'valid' },
      { expression: '\\frac{df1*g1 - f1*\\frac{d(g1)}{dx}}{{g1}^{2}}', status: 'valid' },
      { expression: '\\frac{\\frac{d(f1)}{dx}*g1 - f1*dg1}{{g1}^{2}}', status: 'valid' },
      { expression: '\\frac{df1*g1 - f1*dg1}{{g1}^{2}}', status: 'resolved' },

      { expression: '\\frac{df1*g1 + f1*dg1}{{g1}^{2}}', status: 'invalid' },
      { expression: 'df1*g1 - f1*\\frac{d(g1)}{dx}', status: 'invalid' },
      { expression: '2*\\frac{df1*g1 - f1*dg1}{g1^{2}}', status: 'invalid' },   
    ]
  },
  'f(g)': {
    text: 'f(g)',
    input: '\\frac{d(fr1)}{dx}',
    type: 'derivative',
    steps: [
      { expression: '\\frac{d(fr1)}{dx}', status: 'valid' },
      { expression: 'dfr1*\\frac{d(g1)}{dx}', status: 'valid' },
      { expression: '\\frac{d(g1)}{dx}*dfr1', status: 'valid' },
      { expression: 'dfr1*dg1', status: 'resolved' },
      { expression: 'dg1*dfr1', status: 'resolved' },

      { expression: 'df1*\\frac{d(g1)}{dx}', status: 'invalid' },
      { expression: 'df1', status: 'invalid' },
      { expression: 'dg1', status: 'invalid' },
    ]
  },
  'f+g+h': {
    text: 'f+g+h',
    input: '\\frac{d(f1+g1+h1)}{dx}',
    type: 'derivative',
    steps: [
      { expression: '\\frac{d(f1+g1+h1)}{dx}', status: 'valid' },
      { expression: '\\frac{d(f1)}{dx} + \\frac{d(g1)}{dx} + \\frac{d(h1)}{dx}', status: 'valid' },
      { expression: '\\frac{d(f1)}{dx} + \\frac{d(g1)}{dx} + dh1', status: 'valid' },
      { expression: '\\frac{d(f1)}{dx} + dg1 + dh1', status: 'valid' },
      { expression: 'df1 + dg1 + dh1', status: 'resolved' }
    ]
  },
  'intf*g': {
    text: 'f*g',
    input: '\\int f1*g1',
    type: 'integrate',
    steps: [
      // { expression: '\\int u*v', variables: { u: 'f1', v: 'dg1' }, status: 'valid' },
      {
        expression: 'u(x) * v(x) - \\int (\\frac{d(u(x))}{dx} * v(x))',
        variables: [
          { tag: 'u(x)', value: 'f1' },
          { tag: 'v(x)', value: 'dg1' }
        ],
        status: 'valid'
      }
    ]
  }
}

const executeExpression = async (theoreme, functions, stepCount) => {
  const { input, steps, type } = theoreme;

  // making problem input
  const problem_input = replaceFunctions(input, functions);
  console.log('problem_input to analyze:', problem_input);

  // making problem steps
  const problem_steps = steps.map((step) => ({ ...step, expression: replaceFunctions(step.expression, functions) }));

  // getting problem theorems
  const theorems = type === 'derivative' ?
    JSON.parse(fs.readFileSync(path.resolve(__dirname, './derivative-theorems.json'))) :
    JSON.parse(fs.readFileSync(path.resolve(__dirname, './integrate-theorems.json')));

  // generating math tree
  const math_tree = await generateMathTree({ problem_input, theorems, type });

  // testing each step
  for (let pos = 0; pos < problem_steps.length; pos += 1) {
    // const current_expression = problem_steps[pos].expression;
    const current_expression = problem_steps[pos];
    const expected_status = problem_steps[pos].status;
    const step_list = problem_steps.slice(0, pos).filter((ps) => ['valid', 'resolved'].includes(ps.status)).map((ps) => ps.expression);

    // Hitting math solver
    const result = await testStep({ problem_input, math_tree, theorems, current_expression, step_list, type });

    if (result.exerciseStatus !== expected_status) {
      failedCount += 1;
      console.log(`\x1b[31m[FAIL] ${current_expression.expression}. Result: ${result.exerciseStatus} !== ${expected_status}`);
    } else {
      successCount += 1;
      console.log(`\x1b[32m[OK] ${current_expression.expression}. Result: ${expected_status}`);
    }
  }
  console.log('\x1b[0m');
}

const testStep = async ({ problem_input, math_tree, theorems, current_expression, step_list, type }) => {
  const fullPath = `${mathSolverBasePath}/resolve`;

  const response = await fetch(fullPath, {
    method: 'post',
    body: JSON.stringify({
      type,
      problem_input,
      step_list: JSON.stringify(step_list),
      math_tree,
      theorems,
      current_expression
    }),
    headers: {
      'Content-Type': 'application/json'
    }
  });


  return response.json();
}

const generateMathTree = async ({ problem_input, theorems, type }) => {
  const fullPath = `${mathSolverBasePath}/results/solution-tree`;

  const response = await fetch(fullPath, {
    method: 'post',
    body: JSON.stringify({ problem_input, type, theorems }),
    headers: {
      'Content-Type': 'application/json'
    }
  });

  return response.json();
}

const replaceFunctions = (expression, functions) => {
  let finalExpression = expression;
  functions.forEach((func) => {
    const regex = new RegExp(func.source, 'g');
    finalExpression = finalExpression.replace(regex, func.target);
  });
  
  return finalExpression;
}

const makeFunctionsToExecute = ({ fs: { f, g, h }, variables: { a = 1, b = 1 } }) => {
  const variableA = new RegExp('a1', 'g');
  const variableB = new RegExp('b1', 'g');

  // for +-*/ theoremes
  const dfTarget = f['deriv'].replace(variableA, a).replace(variableB, b);
  const dgTarget = g['deriv'].replace(variableA, a).replace(variableB, b);
  const fTarget = f['func'].replace(variableA, a).replace(variableB, b);
  const gTarget = g['func'].replace(variableA, a).replace(variableB, b);
  // const hTarget = h['func'].replace(variableA, a).replace(variableB, b);
  // const dhTarget = h['deriv'].replace(variableA, a).replace(variableB, b);

  // for f(g) theoremes
  const dfrTarget = f['deriv'].replace(variableA, a).replace(variableB, b).replace('x', `{${gTarget}}`); // TODO: no estoy seguro si {} o () es la que va
  const dgrTarget = g['deriv'].replace(variableA, a).replace(variableB, b).replace('x', `{${fTarget}}`);
  const frTarget = f['func'].replace(variableA, a).replace(variableB, b).replace('x', `{${gTarget}}`);
  const grTarget = g['func'].replace(variableA, a).replace(variableB, b).replace('x', `{${fTarget}}`);

  return [
    { source: 'df1', target: dfTarget },
    { source: 'dg1', target: dgTarget },
    { source: 'f1', target:  fTarget  },
    { source: 'g1', target:  gTarget  },
    // { source: 'dh1', target: dhTarget },
    // { source: 'h1', target:  hTarget  },
    { source: 'dfr1', target: dfrTarget },
    { source: 'dgr1', target: dgrTarget },
    { source: 'fr1', target: frTarget },
    { source: 'gr1', target: grTarget },
  ];
}


// Executing the tests
let successCount = 0;
let failedCount = 0;

const a = 1;
const b = 1;
const theoremesToTest = [
  // 'f+g',
  // 'f-g',
  // 'f*g',
  // 'f/g',
  // 'f(g)',
  // 'f+g+h',
  'intf*g'
];
const functionsToTest = [
  'x',
  'cosx',
  // 'senx',
  // 'tagx',
  // 'sqrt',
  // '1/x',
  // expx
];

const executeFunctions = async ({ theoreme, fs, variables }) => {
  const fsKeys = Object.keys(fs);

  // comparamos que no haya ninguna función igual a otra
  for (const key1 of fsKeys) {
    for (const key2 of fsKeys) {
      if (key1 !== key2 && fs[key1].func === fs[key2].func) {
        return;
      }
    }
  }

  // function logging
  fsKeys.forEach((key) => {
    console.log(`${key}: ${fs[key].func}`);
  });

  const functionsToExecute = makeFunctionsToExecute({ fs, variables });
  return executeExpression(possible_theorems[theoreme], functionsToExecute);
}

const execute = async () => {
  const variables = { a, b };

  for (theoreme of theoremesToTest) {
    console.log(`Executing tests for theoreme: ${theoreme} \n`);

    for (const keyf of functionsToTest) {
      for (const keyg of functionsToTest) {
        const f = functions[keyf];
        const g = functions[keyg];
        const fs = { f, g }

        if (theoreme.includes('h')) {
          for (const keyh of functionsToTest) {
            fs.h = functions[keyh];
            await executeFunctions({ theoreme, fs, variables });
          }
        } else {
          await executeFunctions({ theoreme, fs, variables });
        }
      }
    }
  }

  console.log('Success:', successCount);
  console.log('Failed:', failedCount);
}

execute();


// TODO: bug cuando la primera expresión es igual a la segunda
// TODO: bug cuando existen costantes dentro de la derivada del estilo. a * d(x) <> d(a * x)

// TODO: más ideas de tests que se pueden hacer:
//  - con 3 o más funciones
//  - agregar más casos de funciones equivalente (por ejemplo, diferentes formas de armar polinomios y meterlos en términos separados)
//  - si la función f y g es la misma, multiplicarla por 2 y derivarla
//  - de manera random, simplificar algunas expressiones las variables "a1" y "b1" se multiplican
