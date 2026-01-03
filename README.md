# Claude Code Custom Agents

A collection of 17 custom agents for [Claude Code](https://claude.ai/claude-code) - Anthropic's official CLI tool.

## Agents Overview

| Agent | Description | Model |
|-------|-------------|-------|
| **competitive-intelligence-analyst** | Competitive intelligence and market research specialist. Use for competitor analysis, market positioning, industry trends, business intelligence. | Sonnet |
| **content-marketer** | Content marketing and SEO optimization. Use for blog posts, social media, email campaigns, content calendars. | Sonnet |
| **data-analyst** | Quantitative analysis and statistical insights. Use for numerical data analysis, trends, comparisons, metrics evaluation. | Sonnet |
| **debugger** | Debugging specialist for errors, test failures, and unexpected behavior. Root cause analysis expert. | Sonnet |
| **error-detective** | Log analysis and error pattern detection. Use for debugging, log analysis, production errors, system anomalies. | Sonnet |
| **fact-checker** | Fact verification and source validation. Use for claim verification, source credibility, misinformation detection. | Sonnet |
| **frontend-developer** | Frontend development specialist for React, Vue, Angular, and modern web technologies. | Sonnet |
| **organic-search-analyzer** | Discover top organic Google search results for specific keywords. Returns top 5 organic websites for target keywords. | Opus |
| **prompt-engineer** | Expert prompt optimization for LLMs and AI systems. Use for building AI features, agent performance, system prompts. | Opus |
| **python-pro** | Python expert for clean, performant, idiomatic code. Use for decorators, generators, async/await, optimization. | Sonnet |
| **report-generator** | Transform synthesized research into comprehensive reports. Use after research completion for final document generation. | Sonnet |
| **research-orchestrator** | Coordinate comprehensive research projects. Manages entire research workflow from query clarification to final report. | Opus |
| **search-specialist** | Expert web researcher using advanced search techniques. Masters search operators, result filtering, multi-source verification. | Haiku |
| **seo-analyzer** | SEO analysis and optimization. Use for technical audits, meta tag optimization, Core Web Vitals, schema markup. | Sonnet |
| **serp-content-analyzer** | Analyze why pages rank on Google's first page. Reverse-engineers ranking success via H-tags, content structure, semantic relevance. Hebrew SEO optimized. | Opus |
| **task-decomposition-expert** | Complex goal breakdown specialist. Use for multi-step projects, workflow architecture, tool selection, ChromaDB integration. | Sonnet |
| **ui-ux-designer** | UI/UX design specialist for user-centered design. Use for wireframes, design systems, prototyping, accessibility. | Sonnet |

## Installation

### Option 1: Copy to your Claude config (Recommended)

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/claude-code-agents.git

# Copy agents to Claude Code directory
cp claude-code-agents/agents/*.md ~/.claude/agents/
```

### Option 2: Symlink for easy updates

```bash
git clone https://github.com/YOUR_USERNAME/claude-code-agents.git
cd claude-code-agents
ln -sf $(pwd)/agents/*.md ~/.claude/agents/
```

## Usage

Once installed, agents become available in Claude Code via the Task tool:

```python
# Fact checking
Task(subagent_type="fact-checker", prompt="verify this claim: ...")

# Data analysis
Task(subagent_type="data-analyst", prompt="analyze trends in: ...")

# SEO analysis
Task(subagent_type="seo-analyzer", prompt="audit website: ...")

# Competitive intelligence
Task(subagent_type="competitive-intelligence-analyst", prompt="analyze competitor: ...")

# Research orchestration
Task(subagent_type="research-orchestrator", prompt="research topic: ...")
```

## Agent Categories

### Development
- `debugger` - Error debugging and root cause analysis
- `error-detective` - Log analysis and pattern detection
- `frontend-developer` - Frontend web development
- `python-pro` - Advanced Python development
- `ui-ux-designer` - User interface design

### Research & Analysis
- `data-analyst` - Quantitative data analysis
- `fact-checker` - Claim verification and source validation
- `research-orchestrator` - Research project coordination
- `search-specialist` - Web research and information synthesis
- `competitive-intelligence-analyst` - Market and competitor analysis

### SEO & Marketing
- `content-marketer` - Content marketing and SEO optimization
- `organic-search-analyzer` - Google organic search analysis
- `seo-analyzer` - Technical SEO audits
- `serp-content-analyzer` - SERP content analysis (Hebrew optimized)

### AI & Workflow
- `prompt-engineer` - Prompt optimization for LLMs
- `report-generator` - Research report generation
- `task-decomposition-expert` - Complex workflow orchestration

## Creating Your Own Agents

Agents are markdown files with YAML frontmatter:

```markdown
---
name: your-agent-name
description: What the agent does. Use PROACTIVELY when...
tools: Read, Write, Edit, WebSearch
model: sonnet
---

You are an expert in [domain]...

## Focus Areas
- Area 1
- Area 2

## Approach
1. Step 1
2. Step 2

## Output
- Expected output format
```

### Frontmatter Options

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Agent identifier (lowercase, hyphens) |
| `description` | Yes | What the agent does and when to use it |
| `tools` | No | Comma-separated list of available tools |
| `model` | No | `sonnet` (default), `opus`, or `haiku` |

## Requirements

- [Claude Code](https://claude.ai/claude-code) CLI installed
- Active Claude subscription

## Contributing

1. Fork the repository
2. Create your agent in `agents/`
3. Test with Claude Code
4. Submit a pull request

## License

MIT License - Feel free to use, modify, and distribute.

---

*Created for the Claude Code community*
