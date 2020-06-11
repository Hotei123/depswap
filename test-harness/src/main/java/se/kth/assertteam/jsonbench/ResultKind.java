package se.kth.assertteam.jsonbench;

public enum ResultKind {
	OK,
	PARSE_EXCEPTION,
	PRINT_EXCEPTION,
	CRASH,
	EQUIVALENT_OBJECT,
	NON_EQUIVALENT_OBJECT,
	NULL_OBJECT,
	UNEXPECTED_OBJECT,
	FILE_ERROR;
}
