# Contributing to Resumitory

Thank you for your interest in contributing to Resumitory! We welcome contributions from the community.

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Resumitory.git
   cd Resumitory
   ```
3. **Create a branch** for your feature or bug fix:
   ```bash
   git checkout -b feat/your-feature-name
   ```

## 📋 Development Setup

### Backend Setup

```bash
cd resumitory-backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your Supabase credentials
uvicorn app.main:app --reload
```

### Frontend Setup (Coming Soon)

```bash
cd resumitory-frontend
npm install
cp .env.example .env
# Edit .env with your configuration
npm run dev
```

## 🎯 How to Contribute

### Reporting Bugs

1. **Check existing issues** to avoid duplicates
2. **Create a new issue** with:
   - Clear, descriptive title
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Environment details (OS, Python version, etc.)

### Suggesting Features

1. **Check the roadmap** in `ACTION_PLAN.md`
2. **Create a new issue** with:
   - Clear use case
   - Why it's valuable
   - Proposed implementation (if you have ideas)

### Code Contributions

1. **Pick an issue** or create one first
2. **Comment** on the issue to let others know you're working on it
3. **Write your code** following our style guide
4. **Test thoroughly**
5. **Submit a pull request**

## 📝 Coding Standards

### Python (Backend)

- **Style**: Follow PEP 8
- **Type Hints**: Use type hints everywhere
- **Docstrings**: Add docstrings to all functions/classes
- **Naming**: Use `snake_case` for variables and functions
- **Imports**: Group imports (stdlib, third-party, local)

Example:
```python
from typing import Optional
from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user


async def create_resume(
    name: str,
    user_id: str = Depends(get_current_user)
) -> dict:
    """
    Create a new resume.
    
    Args:
        name: Resume name
        user_id: Authenticated user ID
        
    Returns:
        Dictionary with resume data
    """
    # Implementation
    pass
```

### TypeScript (Frontend)

- **Style**: Use Prettier and ESLint
- **Type Safety**: No `any` types
- **Naming**: Use `camelCase` for variables/functions, `PascalCase` for components
- **Components**: Functional components with hooks

Example:
```typescript
interface ResumeCardProps {
  resumeId: string;
  resumeName: string;
  onDelete: (id: string) => void;
}

export function ResumeCard({ resumeId, resumeName, onDelete }: ResumeCardProps) {
  // Implementation
}
```

## 📦 Commit Messages

Use **Conventional Commits** format:

```
<type>: <description>

[optional body]

[optional footer]
```

### Types

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code formatting (no logic change)
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Build process or tools
- `perf:` Performance improvements
- `security:` Security fixes

### Examples

```bash
feat: Add resume upload with drag-and-drop support

- Implement file upload component
- Add drag-and-drop functionality
- Support PDF and .tex files
- Add file size validation
```

```bash
fix: Resolve authentication token expiration issue

Token was not being refreshed properly, causing 401 errors
after 1 hour. Now tokens are refreshed automatically.

Fixes #123
```

## 🧪 Testing

### Backend Tests

```bash
cd resumitory-backend
pytest tests/
```

### Frontend Tests (Coming Soon)

```bash
cd resumitory-frontend
npm test
```

### Manual Testing

1. Test happy paths (normal usage)
2. Test edge cases (empty inputs, large files, etc.)
3. Test error scenarios (network failures, invalid data)
4. Test on different browsers/devices

## 🔍 Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new features
3. **Ensure all tests pass**
4. **Update CHANGELOG.md** if applicable
5. **Fill out the PR template**

### PR Checklist

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] No new warnings
- [ ] Commit messages follow convention

## 🚫 What NOT to Contribute

We're focused on core features. Please avoid:

- ❌ AI resume generation features
- ❌ ATS optimization tools
- ❌ Job board scrapers
- ❌ Social networking features
- ❌ Mobile apps (focus on web first)

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [Supabase Documentation](https://supabase.com/docs)
- [Action Plan](ACTION_PLAN.md)
- [Project Blueprint](kickoff.md)

## 💬 Communication

- **GitHub Issues**: For bugs and features
- **Pull Requests**: For code contributions
- **Discussions**: For questions and ideas

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Thank You!

Every contribution helps make Resumitory better for job seekers everywhere.

**Remember**: Perfect is the enemy of done. Ship fast, iterate faster! 🚀
