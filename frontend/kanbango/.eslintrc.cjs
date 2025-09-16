// .eslintrc.cjs
module.exports = {
    // 指定脚本的运行环境
    env: {
        browser: true,
        es2021: true,
        node: true,
    },
    // 继承的规则集
    extends: [
        'eslint:recommended',
        'plugin:vue/vue3-essential', // Vue 3 基础规则
        'prettier', // !! 必须放在最后，用于覆盖eslint的格式规则
    ],
    // ESLint 解析器选项
    parserOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module',
    },
    // 使用的插件
    plugins: ['vue', 'prettier'],
    // 自定义规则
    rules: {
        'prettier/prettier': 'error', // 将 Prettier 的规则作为 ESLint 错误来报告
    },
};