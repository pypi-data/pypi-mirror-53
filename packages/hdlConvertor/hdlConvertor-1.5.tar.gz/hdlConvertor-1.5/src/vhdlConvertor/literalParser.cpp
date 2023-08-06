#include <vector>
#include <stdlib.h>
#include <string.h>
#include <algorithm>

#include <hdlConvertor/notImplementedLogger.h>
#include <hdlConvertor/vhdlConvertor/literalParser.h>
#include <hdlConvertor/vhdlConvertor/referenceParser.h>

namespace hdlConvertor {
namespace vhdl {

using vhdlParser = vhdl_antlr::vhdlParser;
using namespace hdlConvertor::hdlObjects;

std::unique_ptr<iHdlExpr> VhdlLiteralParser::visitBIT_STRING_LITERAL(
		const std::string &_s) {
	std::string s = _s;
	std::size_t fdRadix = s.find('"') - 1;
	std::transform(s.begin(), s.end(), s.begin(), ::tolower);
	int radix = 0;
	int bitRatio = 0;
	switch (s[fdRadix]) {
	case 'b':
		radix = 2;
		bitRatio = 1;
		break;
	case 'o':
		radix = 8;
		bitRatio = 2;
		break;
	case 'x':
		radix = 16;
		bitRatio = 4;
		break;
	case 'd':
		radix = 16;
		bitRatio = 4;
		break;
	}

	int bits = 0;
	if ((fdRadix > 0 && s[fdRadix - 1] != 'u')
			|| (fdRadix > 1 && s[fdRadix - 1] == 'u')) {
		bits = std::stoi(s);
	}

	s[s.length() - 1] = 0; // cut of "
	s.erase(std::remove(s.begin(), s.end(), '_'), s.end());
	const char *strVal = (char*) s.c_str() + fdRadix + 2; // cut off radix"
	if (bits == 0) {
		bits = strlen(strVal) * bitRatio;
	}

	return iHdlExpr::INT(strVal, bits, radix);
}

std::unique_ptr<iHdlExpr> VhdlLiteralParser::visitNumeric_literal(
		vhdlParser::Numeric_literalContext *ctx) {
	// numeric_literal: // name there means name of unit, but there is ambiguity with any other name
	//       DECIMAL_LITERAL (name)?
	//       | BASED_LITERAL (name)?
	//       | name
	// ;
	std::unique_ptr<iHdlExpr> name = nullptr;
	auto _n = ctx->name();
	if (_n)
		name = VhdlReferenceParser::visitName(_n);
	auto _dl = ctx->DECIMAL_LITERAL();
	if (_dl) {
		auto dl = visitDECIMAL_LITERAL(_dl);
		if (name) {
			return std::make_unique<iHdlExpr>(move(dl), HdlOperatorType::MUL,
					move(name));
		} else {
			return dl;
		}
	}
	auto _bl = ctx->BASED_LITERAL();
	if (_bl) {
		auto bl = visitBASED_LITERAL(_bl);
		if (name) {
			return std::make_unique<iHdlExpr>(move(bl), HdlOperatorType::MUL,
					move(name));
		} else {
			return bl;
		}
	}
	assert(name);
	return name;
}
std::unique_ptr<iHdlExpr> VhdlLiteralParser::visitPhysical_literal(
		vhdlParser::Physical_literalContext *ctx) {
	// physical_literal: ( DECIMAL_LITERAL |  BASED_LITERAL )? name;
	auto _n = ctx->name();
	auto name = VhdlReferenceParser::visitName(_n);
	auto _dl = ctx->DECIMAL_LITERAL();
	if (_dl) {
		auto dl = visitDECIMAL_LITERAL(_dl);
		return std::make_unique<iHdlExpr>(std::move(dl), HdlOperatorType::MUL, std::move(name));
	}
	auto _bl = ctx->BASED_LITERAL();
	if (_bl) {
		auto bl = visitBASED_LITERAL(_bl);
		return std::make_unique<iHdlExpr>(std::move(bl), HdlOperatorType::MUL, std::move(name));
	}
	return name;
}
std::unique_ptr<iHdlExpr> VhdlLiteralParser::visitDECIMAL_LITERAL(
		antlr4::tree::TerminalNode *ctx) {
	// decimal_literal: integer ( DOT integer )? ( exponent )?;
	auto n = ctx->getText();
	bool is_float = false;
	for (auto c : n) {
		if (c == '.' || c == 'e' || c == 'E') {
			is_float = true;
			break;
		}
	}
	if (is_float)
		return iHdlExpr::FLOAT(atof(n.c_str()));
	else {
		auto _n = atoi(n.c_str());
		return iHdlExpr::INT(_n);
	}
}
std::unique_ptr<iHdlExpr> VhdlLiteralParser::visitBASED_LITERAL(
		antlr4::tree::TerminalNode *ctx) {
	// BASED_LITERAL:
	//       BASE HASHTAG BASED_INTEGER ( DOT BASED_INTEGER )? HASHTAG ( EXPONENT )?
	// ;

	// INTEGER must be checked to be between and including 2 and 16
	// (included) i.e. INTEGER >=2 and INTEGER <=16
	// A Based integer (a number without a . such as 3) should not have a
	// negative exponent A Based fractional number with a . i.e. 3.0 may
	// have a negative exponent These should be checked in the
	// Visitor/Listener whereby an appropriate error message
	// should be given

	auto bl = ctx->getText();
	auto ht0_pos = bl.find('#');
	auto ht1_pos = bl.find('#', ht0_pos + 1);
	auto dot_pos = bl.find('.', ht0_pos + 1);
	auto _base = bl.substr(0, ht0_pos);
	int base = atoi(_base.c_str());
	BigInteger val = BigInteger(bl.substr(ht0_pos, ht1_pos - ht0_pos), base);
	if (dot_pos != std::string::npos) {
		NotImplementedLogger::print(
				"LiteralParser.visitBased_literal - decimal part", ctx);
	}

	if (ht1_pos != bl.size() - 1) {
		NotImplementedLogger::print(
				"LiteralParser.visitBased_literal - EXPONENT", ctx);
	}
	return std::make_unique<iHdlExpr>(val);
}

std::unique_ptr<iHdlExpr> VhdlLiteralParser::visitEnumeration_literal(
		vhdlParser::Enumeration_literalContext *ctx) {
	// enumeration_literal: identifier | character_literal;
	auto id = ctx->identifier();
	if (id)
		return visitIdentifier(id);

	auto _cl = ctx->CHARACTER_LITERAL()->getText();
	auto cl = visitCHARACTER_LITERAL(_cl);
	dynamic_cast<HdlValue*>(cl->data)->bits = 8;
	return cl;
}
std::unique_ptr<iHdlExpr> VhdlLiteralParser::visitSTRING_LITERAL(
		const std::string &ctx) {
	std::string str = ctx.substr(1, ctx.length() - 2);
	auto replace_all = [](std::string &data, const std::string &to_search,
			const std::string &replace_str) {
		size_t pos = data.find(to_search);
		while (pos != std::string::npos) {
			data.replace(pos, to_search.size(), replace_str);
			pos = data.find(to_search, pos + replace_str.size());
		}
	};
	replace_all(str, "\"\"", "\"");
	return iHdlExpr::STR(str);
}
std::unique_ptr<iHdlExpr> VhdlLiteralParser::visitCHARACTER_LITERAL(
		const std::string &ctx) {
	return iHdlExpr::INT(ctx.substr(1, 1), BigInteger::CHAR_BASE);
}
std::unique_ptr<iHdlExpr> VhdlLiteralParser::visitIdentifier(
		vhdlParser::IdentifierContext *ctx) {
	return iHdlExpr::ID(getIdentifierStr(ctx));
}
std::string VhdlLiteralParser::getIdentifierStr(
		vhdlParser::IdentifierContext *ctx) {
	return ctx->getText();
}
bool VhdlLiteralParser::isStrDesignator(vhdlParser::DesignatorContext *ctx) {
	// designator: identifier | operator_symbol
	return ctx->identifier() == nullptr;
}
std::string VhdlLiteralParser::visitDesignator(
		vhdlParser::DesignatorContext *ctx) {
	// designator: identifier | operator_symbol
	// operator_symbol: STRING_LITERAL;
	if (isStrDesignator(ctx)) {
		return ctx->operator_symbol()->STRING_LITERAL()->getText();
	} else {
		return getIdentifierStr(ctx->identifier());
	}
}

std::string VhdlLiteralParser::visitLabel(vhdlParser::LabelContext *ctx) {
	// label_colon
	// : identifier COLON
	// ;
	return getIdentifierStr(ctx->identifier());
}

}
}
