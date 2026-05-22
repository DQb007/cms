import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from '@/App.vue'
import { router } from '@/router'
import '@/styles/main.css'

console.log(
  '%c你在电脑前看这段文字，\n写文字的人正在等你。\n学无止境，\n需要课程请添加微信：DQbhxs',
  [
    'display: inline-block',
    'font-size: 24px',
    'line-height: 1.55',
    'font-family: "Microsoft YaHei", "PingFang SC", sans-serif',
    'font-weight: 700',
    'color: #eaf6ff',
    'background: linear-gradient(135deg, #10243f, #123a62)',
    'border-left: 6px solid #20d6b5',
    'border-radius: 6px',
    'padding: 12px 18px',
    'box-shadow: 0 8px 24px rgba(16, 36, 63, 0.24)',
  ].join(';'),
)

const app = createApp(App)

app.use(createPinia()).use(router).mount('#app')
