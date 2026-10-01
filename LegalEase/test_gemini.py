from ai_core.gemini_generator import GeminiDocumentGenerator

generator = GeminiDocumentGenerator()

result = generator.generate_document(
    document_type="Non-Disclosure Agreement",
    parties="Company: ABC Technologies, Employee: John",
    terms="The employee must keep company confidential information private.",
    dates="Effective Date: 30 September 2026"
)

print("\n===== GENERATED DOCUMENT =====\n")
print(result)