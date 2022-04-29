/**
 * Autogenerated by Thrift Compiler (0.15.0)
 *
 * DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
 *  @generated
 */
#include "CodeChat_Services_types.h"

#include <algorithm>
#include <ostream>

#include <thrift/TToString.h>



int _kCodeChatClientLocationValues[] = {
  CodeChatClientLocation::url,
  CodeChatClientLocation::html,
  CodeChatClientLocation::browser
};
const char* _kCodeChatClientLocationNames[] = {
  "url",
  "html",
  "browser"
};
const std::map<int, const char*> _CodeChatClientLocation_VALUES_TO_NAMES(::apache::thrift::TEnumIterator(3, _kCodeChatClientLocationValues, _kCodeChatClientLocationNames), ::apache::thrift::TEnumIterator(-1, nullptr, nullptr));

std::ostream& operator<<(std::ostream& out, const CodeChatClientLocation::type& val) {
  std::map<int, const char*>::const_iterator it = _CodeChatClientLocation_VALUES_TO_NAMES.find(val);
  if (it != _CodeChatClientLocation_VALUES_TO_NAMES.end()) {
    out << it->second;
  } else {
    out << static_cast<int>(val);
  }
  return out;
}

std::string to_string(const CodeChatClientLocation::type& val) {
  std::map<int, const char*>::const_iterator it = _CodeChatClientLocation_VALUES_TO_NAMES.find(val);
  if (it != _CodeChatClientLocation_VALUES_TO_NAMES.end()) {
    return std::string(it->second);
  } else {
    return std::to_string(static_cast<int>(val));
  }
}


RenderClientReturn::~RenderClientReturn() noexcept {
}


void RenderClientReturn::__set_html(const std::string& val) {
  this->html = val;
}

void RenderClientReturn::__set_id(const int32_t val) {
  this->id = val;
}

void RenderClientReturn::__set_error(const std::string& val) {
  this->error = val;
}
std::ostream& operator<<(std::ostream& out, const RenderClientReturn& obj)
{
  obj.printTo(out);
  return out;
}


uint32_t RenderClientReturn::read(::apache::thrift::protocol::TProtocol* iprot) {

  ::apache::thrift::protocol::TInputRecursionTracker tracker(*iprot);
  uint32_t xfer = 0;
  std::string fname;
  ::apache::thrift::protocol::TType ftype;
  int16_t fid;

  xfer += iprot->readStructBegin(fname);

  using ::apache::thrift::protocol::TProtocolException;


  while (true)
  {
    xfer += iprot->readFieldBegin(fname, ftype, fid);
    if (ftype == ::apache::thrift::protocol::T_STOP) {
      break;
    }
    switch (fid)
    {
      case 1:
        if (ftype == ::apache::thrift::protocol::T_STRING) {
          xfer += iprot->readString(this->html);
          this->__isset.html = true;
        } else {
          xfer += iprot->skip(ftype);
        }
        break;
      case 2:
        if (ftype == ::apache::thrift::protocol::T_I32) {
          xfer += iprot->readI32(this->id);
          this->__isset.id = true;
        } else {
          xfer += iprot->skip(ftype);
        }
        break;
      case 3:
        if (ftype == ::apache::thrift::protocol::T_STRING) {
          xfer += iprot->readString(this->error);
          this->__isset.error = true;
        } else {
          xfer += iprot->skip(ftype);
        }
        break;
      default:
        xfer += iprot->skip(ftype);
        break;
    }
    xfer += iprot->readFieldEnd();
  }

  xfer += iprot->readStructEnd();

  return xfer;
}

uint32_t RenderClientReturn::write(::apache::thrift::protocol::TProtocol* oprot) const {
  uint32_t xfer = 0;
  ::apache::thrift::protocol::TOutputRecursionTracker tracker(*oprot);
  xfer += oprot->writeStructBegin("RenderClientReturn");

  xfer += oprot->writeFieldBegin("html", ::apache::thrift::protocol::T_STRING, 1);
  xfer += oprot->writeString(this->html);
  xfer += oprot->writeFieldEnd();

  xfer += oprot->writeFieldBegin("id", ::apache::thrift::protocol::T_I32, 2);
  xfer += oprot->writeI32(this->id);
  xfer += oprot->writeFieldEnd();

  xfer += oprot->writeFieldBegin("error", ::apache::thrift::protocol::T_STRING, 3);
  xfer += oprot->writeString(this->error);
  xfer += oprot->writeFieldEnd();

  xfer += oprot->writeFieldStop();
  xfer += oprot->writeStructEnd();
  return xfer;
}

void swap(RenderClientReturn &a, RenderClientReturn &b) {
  using ::std::swap;
  swap(a.html, b.html);
  swap(a.id, b.id);
  swap(a.error, b.error);
  swap(a.__isset, b.__isset);
}

RenderClientReturn::RenderClientReturn(const RenderClientReturn& other0) {
  html = other0.html;
  id = other0.id;
  error = other0.error;
  __isset = other0.__isset;
}
RenderClientReturn& RenderClientReturn::operator=(const RenderClientReturn& other1) {
  html = other1.html;
  id = other1.id;
  error = other1.error;
  __isset = other1.__isset;
  return *this;
}
void RenderClientReturn::printTo(std::ostream& out) const {
  using ::apache::thrift::to_string;
  out << "RenderClientReturn(";
  out << "html=" << to_string(html);
  out << ", " << "id=" << to_string(id);
  out << ", " << "error=" << to_string(error);
  out << ")";
}

