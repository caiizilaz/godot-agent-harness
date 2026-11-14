import type { Locale } from './site-content';
export const HARNESS = {
  "th": {
    "category": "เครื่องมือสำหรับนักพัฒนา",
    "title": "Godot Agent Harness",
    "lead": "จากบทเรียนการสร้างเกม สู่ workflow ที่นำไปใช้ต่อได้",
    "summary": "SPACE8 LABS สกัดบทเรียนจาก TKR และ HMP เป็นเครื่องมือทำงานร่วมกับ AI agents: แบ่งขอบเขตงาน ตรวจผลจริง และส่งต่องานพร้อมหลักฐาน",
    "cta": "ดูแนวทางและตัวอย่าง",
    "repo": "เปิดซอร์สโค้ด",
    "origin": "พัฒนาจากงานเกมของเรา",
    "status": "กำลังพัฒนา",
    "steps": [
      "กำหนดขอบเขต",
      "ทำใน worktree",
      "ตรวจผล",
      "ส่งต่อหลักฐาน"
    ],
    "sections": [
      [
        "ปัญหาที่พบในงานจริง",
        "งานหลายส่วนใช้ไฟล์ร่วมกัน การ import ที่ไม่สมบูรณ์ทำให้การตรวจผิดพลาด และงานที่ผ่านเทสต์อาจยังแสดงผลไม่ถูกต้อง"
      ],
      [
        "วิธีทำงาน",
        "กำหนดผู้รับผิดชอบและ contract ต่อชิ้นงาน แยก worktree รันการตรวจที่มีขอบเขตเวลาและ log และแนบภาพเมื่อเปลี่ยนสิ่งที่ผู้เล่นเห็น"
      ],
      [
        "ขยายออกจาก Godot",
        "แยกแกน workflow ออกจาก adapter สำหรับ engine ใช้ Godot เป็นตัวอย่างแรก และคำสั่งทั่วไปสำหรับงาน Node/TypeScript การรองรับ engine อื่นต้องผ่านการทดลองก่อน"
      ],
      [
        "วัดผลอย่างตรงไปตรงมา",
        "เป้าหมายคือคุณภาพงานที่ดีขึ้นและลดเวลาหรือ token ที่เสียไป ยังไม่มีตัวเลขยืนยันการประหยัด token ข้ามโมเดล และไม่อ้างผลจากการทดลองเครื่องมือว่าเป็นผลของ AI ทั้ง workflow"
      ]
    ]
  },
  "en": {
    "category": "Developer tools",
    "title": "Godot Agent Harness",
    "lead": "Lessons from building games, made reusable",
    "summary": "SPACE8 LABS turns lessons from TKR and HMP into a workflow for AI-assisted development: bounded ownership, verified checks and evidence-based handoffs.",
    "cta": "Explore the workflow",
    "repo": "View source code",
    "origin": "Built from our game projects",
    "status": "In development",
    "steps": [
      "Define scope",
      "Isolate work",
      "Verify results",
      "Hand off evidence"
    ],
    "sections": [
      [
        "The problem in practice",
        "Parallel tasks share files, incomplete imports undermine checks, and passing logic tests do not prove that a screen renders correctly."
      ],
      [
        "The workflow",
        "Define ownership and contracts per task, isolate changes in worktrees, bound check time and log size, and inspect screenshots when player-visible output changes."
      ],
      [
        "Beyond Godot",
        "Separate the workflow core from engine adapters. Godot is the first example; generic commands support Node/TypeScript tasks. Other engines need their own validation before support is claimed."
      ],
      [
        "Measured claims",
        "The aim is better work with less wasted time and context. Cross-model token savings have not been established. Tool-level fixtures are not evidence of end-to-end AI productivity."
      ]
    ]
  },
  "zh": {
    "category": "开发者工具",
    "title": "Godot Agent Harness",
    "lead": "将游戏开发经验转化为可复用的工作流程",
    "summary": "SPACE8 LABS 将 TKR 和 HMP 的开发经验整理为 AI 辅助开发流程：明确任务范围、验证检查结果，并附带证据交接工作。",
    "cta": "了解工作流程",
    "repo": "查看源代码",
    "origin": "源自我们的游戏项目",
    "status": "开发中",
    "steps": [
      "明确范围",
      "隔离工作",
      "验证结果",
      "交接证据"
    ],
    "sections": [
      [
        "实际遇到的问题",
        "并行任务会修改同一文件，不完整的资源导入会影响检查结果，而逻辑测试通过并不能证明画面显示正确。"
      ],
      [
        "工作方式",
        "为每个任务定义文件归属与接口约定，使用独立工作树，限制检查时间与日志大小，并在玩家可见内容变更后检查截图。"
      ],
      [
        "扩展到 Godot 之外",
        "将通用工作流程与引擎适配器分离。以 Godot 为首个示例，通过通用命令支持 Node/TypeScript 任务。其他引擎必须经过验证后才能声明支持。"
      ],
      [
        "如实衡量效果",
        "目标是提高质量，减少浪费的时间和上下文。目前尚未验证跨模型的 token 节省效果。工具级测试不能代表完整 AI 开发流程的生产力。"
      ]
    ]
  }
} satisfies Record<Locale, {category:string;title:string;lead:string;summary:string;cta:string;repo:string;origin:string;status:string;steps:string[];sections:string[][]}>;
